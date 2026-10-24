#!/usr/bin/env python3
"""Importa el contenido publicado en el sitio actual a site/pages/ (solo stdlib).

Recorre sitemap.xml (incluye sitemap index), descarga cada URL, extrae título,
descripción, fechas y el contenido principal, y escribe una página con front
matter conservando la MISMA ruta (sin cambio de URLs → sin pérdida de ranking).

Uso: python3 site/import_existing.py [https://drcorujo.uy] [--overwrite]
"""
import html
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

PAGES = Path(__file__).parent / "pages"
UA = {"User-Agent": "Mozilla/5.0 (drcorujo-import)"}
SKIP_TAGS = {"script", "style", "noscript", "nav", "header", "footer", "form", "svg", "iframe", "aside"}
KEEP_TAGS = {"h2", "h3", "h4", "p", "ul", "ol", "li", "strong", "em", "b", "i", "a",
             "blockquote", "table", "thead", "tbody", "tr", "th", "td", "br", "img", "figure", "figcaption"}
ARTICLE_HINTS = ("/blog/", "/articulos/", "/articulo/", "/posts/", "/post/", "/noticias/")


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")


def sitemap_urls(url):
    root = ElementTree.fromstring(fetch(url))
    locs = [e.text.strip() for e in root.iter() if e.tag.endswith("loc") and e.text]
    if root.tag.endswith("sitemapindex"):
        return [u for child in locs for u in sitemap_urls(child)]
    return locs


class Extractor(HTMLParser):
    """Toma <main>/<article> si existen; si no, <body>. Deja solo HTML semántico."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.jsonld, self.title, self.h1 = {}, [], "", ""
        self.out, self.skip, self.scope = [], 0, None
        self._in_title = self._in_h1 = self._in_ld = False
        self._ld_buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key and "content" in a:
                self.meta[key.lower()] = a["content"]
        elif tag == "title":
            self._in_title = True
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True
        if tag in ("main", "article") and self.scope is None:
            self.scope, self.out = tag, []
        if tag in SKIP_TAGS:
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "h1":
            self._in_h1 = True
            return
        if tag in KEEP_TAGS:
            keep = {k: v for k, v in a.items() if k in ("href", "src", "alt") and v}
            attrs_s = "".join(f' {k}="{html.escape(v)}"' for k, v in keep.items())
            self.out.append(f"<{tag}{attrs_s}>")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_ld:
            self._in_ld = False
            try:
                self.jsonld.append(json.loads("".join(self._ld_buf)))
            except ValueError:
                pass
            self._ld_buf = []
        if tag in SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == "h1":
            self._in_h1 = False
        elif tag in KEEP_TAGS and tag not in ("br", "img"):
            self.out.append(f"</{tag}>")
        if tag == self.scope:
            self.scope = "done"

    def handle_data(self, data):
        if self._in_ld:
            self._ld_buf.append(data)
        elif self._in_title:
            self.title += data
        elif self._in_h1:
            self.h1 += data
        elif not self.skip and self.scope != "done":
            self.out.append(html.escape(data))


def find_dates(jsonld):
    found = {}

    def walk(o):
        if isinstance(o, dict):
            for k in ("datePublished", "dateModified"):
                if k in o and k not in found:
                    found[k] = str(o[k])[:10]
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(jsonld)
    return found


def tidy(body):
    body = re.sub(r"<(\w+)>\s*</\1>", "", body)          # etiquetas vacías
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r"\s*\n\s*", "\n", body)
    body = re.sub(r"(</(?:p|h2|h3|h4|ul|ol|li|blockquote|table|figure)>)", r"\1\n", body)
    return body.strip()


def import_url(url, base, overwrite):
    path = "/" + url.replace(base, "", 1).strip("/")
    path = "/" if path == "/" else path + "/"
    if path == "/":
        return None  # la home se mantiene con el template answer-first
    target = PAGES / (path.strip("/") + ".html")
    if target.exists() and not overwrite:
        return f"skip (existe) {path}"
    p = Extractor()
    p.feed(fetch(url))
    dates = find_dates(p.jsonld)
    is_article = any(h in path for h in ARTICLE_HINTS) or p.meta.get("og:type") == "article"
    published = (dates.get("datePublished") or p.meta.get("article:published_time", "")[:10]) or None
    modified = dates.get("dateModified") or p.meta.get("article:modified_time", "")[:10] or published
    title = (p.meta.get("og:title") or p.title or p.h1).strip()
    meta = {
        "title": title,
        "description": (p.meta.get("description") or p.meta.get("og:description") or "").strip(),
        "path": path,
        "type": "article" if is_article else "page",
        "crumb": (p.h1 or title).strip(),
        "medical": True,
        # Contenido ya publicado por el Dr. Corujo: se mantiene indexado.
        "reviewed": True,
        "last_reviewed": modified or "",
        "imported_from": url,
    }
    if is_article:
        meta["date_published"] = published or "2000-01-01"
        if modified:
            meta["date_modified"] = modified
    h1 = html.escape((p.h1 or title).strip())
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        f"<!--{json.dumps(meta, ensure_ascii=False, indent=1)}-->\n<h1>{h1}</h1>\n{tidy(''.join(p.out))}\n",
        encoding="utf-8")
    return f"ok {path}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    base = (args[0] if args else "https://drcorujo.uy").rstrip("/")
    overwrite = "--overwrite" in sys.argv
    urls = sitemap_urls(base + "/sitemap.xml")
    print(f"{len(urls)} URLs en sitemap")
    for u in urls:
        try:
            r = import_url(u, base, overwrite)
            if r:
                print(r)
        except Exception as e:  # una página rota no frena el resto
            print(f"ERROR {u}: {e}", file=sys.stderr)
    print("\nRevisar cada página: agregar párrafo 'answer' al inicio y TL;DR por sección.")


if __name__ == "__main__":
    main()
