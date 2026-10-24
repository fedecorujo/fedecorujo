#!/usr/bin/env python3
"""Generador estático de drcorujo.uy (solo stdlib).

Lee config.json (NAP/entidad) + pages/**/*.html (front matter JSON en el primer
comentario) y escribe dist/ con HTML, JSON-LD, sitemap.xml, robots.txt, llms.txt.

Uso: python3 site/build.py [--strict]
  --strict  falla si quedan TODO en config o páginas sin revisión médica.
"""
import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT.parent / "dist"
FRONT_MATTER = re.compile(r"\A<!--\s*(\{.*?\})\s*-->\s*", re.S)

# Crawlers de buscadores e IA explícitamente permitidos (GEO).
AI_BOTS = [
    "Googlebot", "Bingbot", "Google-Extended", "GPTBot", "OAI-SearchBot",
    "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User",
    "PerplexityBot", "Perplexity-User", "Applebot", "Applebot-Extended",
    "meta-externalagent", "DuckAssistBot", "CCBot",
]


def is_todo(value):
    return isinstance(value, str) and value.strip().upper().startswith("TODO")


def clean(obj):
    """Elimina recursivamente valores TODO/vacíos para no publicar schema inválido."""
    if isinstance(obj, dict):
        out = {k: clean(v) for k, v in obj.items()}
        return {k: v for k, v in out.items() if v not in (None, "", [], {})}
    if isinstance(obj, list):
        out = [clean(v) for v in obj]
        return [v for v in out if v not in (None, "", [], {})]
    return None if is_todo(obj) else obj


def find_todos(obj, path="config"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not k.startswith("_"):
                yield from find_todos(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from find_todos(v, f"{path}[{i}]")
    elif is_todo(obj):
        yield path


def load_pages():
    pages = []
    for f in sorted((ROOT / "pages").rglob("*.html")):
        raw = f.read_text(encoding="utf-8")
        m = FRONT_MATTER.match(raw)
        if not m:
            sys.exit(f"{f}: falta front matter JSON")
        meta = json.loads(m.group(1))
        meta["body"] = raw[m.end():]
        meta["source"] = f.relative_to(ROOT)
        pages.append(meta)
    return pages


def entity_graph(cfg):
    url = cfg["site_url"]
    addr = cfg["address"]
    person = {
        "@type": "Person",
        "@id": f"{url}/#person",
        "name": cfg["name"],
        "givenName": cfg["given_name"],
        "familyName": cfg["family_name"],
        "honorificPrefix": cfg["honorific_prefix"],
        "jobTitle": cfg["job_title"],
        "description": cfg["description"],
        "image": url + cfg["image"],
        "url": f"{url}/sobre-mi/",
        "knowsAbout": cfg["knows_about"],
        "knowsLanguage": ["es", "en"],
        "alumniOf": [{"@type": "CollegeOrUniversity", **o} for o in cfg["alumni_of"]],
        "memberOf": [{"@type": "MedicalOrganization", **o} for o in cfg["member_of"]],
        "hasCredential": {"@type": "EducationalOccupationalCredential",
                          "credentialCategory": "Licencia médica",
                          "identifier": cfg["license"]},
        "worksFor": {"@id": f"{url}/#physician"},
        "sameAs": cfg["same_as"],
    }
    physician = {
        "@type": "IndividualPhysician",
        "@id": f"{url}/#physician",
        "name": cfg["name"],
        "url": url + "/",
        "image": url + cfg["image"],
        "description": cfg["description"],
        "medicalSpecialty": f"https://schema.org/{cfg['medical_specialty']}",
        "telephone": cfg["telephone"],
        "email": cfg["email"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": addr["street"],
            "addressLocality": addr["locality"],
            "addressRegion": addr["region"],
            "postalCode": addr["postal_code"],
            "addressCountry": addr["country"],
        },
        "geo": ({"@type": "GeoCoordinates", "latitude": cfg["geo"]["lat"],
                 "longitude": cfg["geo"]["lng"]} if cfg["geo"]["lat"] else None),
        "openingHours": cfg["opening_hours"],
        "areaServed": {"@type": "Country", "name": "Uruguay"},
        "hospitalAffiliation": [{"@type": "Hospital", **h} for h in cfg["hospital_affiliations"]],
        "availableService": [
            {"@type": "MedicalProcedure", "name": "Cirugía de cataratas (facoemulsificación)",
             "url": f"{url}/cirugia-de-cataratas/"},
        ],
        "employee": {"@id": f"{url}/#person"},
        "sameAs": [s for s in cfg["same_as"] if "g.page" in s or "google" in s],
    }
    website = {
        "@type": "WebSite",
        "@id": f"{url}/#website",
        "url": url + "/",
        "name": cfg["name"],
        "inLanguage": cfg["lang"],
        "publisher": {"@id": f"{url}/#person"},
    }
    return [website, person, physician]


def page_graph(cfg, page, today):
    url = cfg["site_url"]
    page_url = url + page["path"]
    graph = entity_graph(cfg)
    webpage = {
        "@type": "MedicalWebPage" if page["type"] in ("service", "faq", "article") else
                 ("AboutPage" if page["type"] == "about" else
                  "ContactPage" if page["type"] == "contact" else "WebPage"),
        "@id": f"{page_url}#webpage",
        "url": page_url,
        "name": page["title"],
        "description": page["description"],
        "inLanguage": cfg["lang"],
        "isPartOf": {"@id": f"{url}/#website"},
        "about": {"@id": f"{url}/#physician"} if page["type"] in ("home", "about", "contact") else
                 page.get("about"),
        "author": {"@id": f"{url}/#person"},
        "reviewedBy": {"@id": f"{url}/#person"} if page.get("reviewed") else None,
        "lastReviewed": page.get("last_reviewed") if page.get("reviewed") else None,
        "dateModified": page.get("date_modified", today),
        "breadcrumb": {"@id": f"{page_url}#breadcrumb"},
    }
    graph.append(webpage)

    crumbs = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": url + "/"}]
    if page["path"] != "/":
        parts = [p for p in page["path"].strip("/").split("/")]
        if len(parts) > 1:
            crumbs.append({"@type": "ListItem", "position": 2, "name": "Artículos",
                           "item": f"{url}/{parts[0]}/"})
        crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1,
                       "name": page.get("crumb", page["title"]), "item": page_url})
    graph.append({"@type": "BreadcrumbList", "@id": f"{page_url}#breadcrumb",
                  "itemListElement": crumbs})

    if page.get("faq"):
        graph.append({
            "@type": "FAQPage",
            "@id": f"{page_url}#faq",
            "mainEntity": [{"@type": "Question", "name": q["q"],
                            "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                           for q in page["faq"]],
        })

    if page["type"] == "article":
        graph.append({
            "@type": "Article",
            "@id": f"{page_url}#article",
            "headline": page["title"],
            "description": page["description"],
            "mainEntityOfPage": {"@id": f"{page_url}#webpage"},
            "author": {"@id": f"{url}/#person"},
            "publisher": {"@id": f"{url}/#person"},
            "datePublished": page["date_published"],
            "dateModified": page.get("date_modified", page["date_published"]),
            "inLanguage": cfg["lang"],
            "citation": page.get("sources", []),
        })
    return clean({"@context": "https://schema.org", "@graph": graph})


def render_faq(faq):
    items = "\n".join(
        f'<details><summary><h3>{html.escape(q["q"])}</h3></summary>'
        f'<p>{html.escape(q["a"])}</p></details>' for q in faq)
    return f'<section class="faq" aria-label="Preguntas frecuentes">\n{items}\n</section>'


def render_articles(pages):
    arts = sorted((p for p in pages if p["type"] == "article"),
                  key=lambda p: p["date_published"], reverse=True)
    lis = "\n".join(
        f'<li><a href="{p["path"]}">{html.escape(p["title"])}</a>'
        f'<p>{html.escape(p["description"])}</p></li>' for p in arts)
    return f'<ul class="articles">\n{lis}\n</ul>'


def contact_links(cfg):
    links = []
    if not is_todo(cfg["whatsapp"]):
        links.append(f'<a class="btn" href="https://wa.me/{cfg["whatsapp"]}">WhatsApp</a>')
    if not is_todo(cfg["booking_url"]):
        links.append(f'<a class="btn" href="{cfg["booking_url"]}">Agendar consulta</a>')
    if not is_todo(cfg["telephone"]):
        tel = re.sub(r"[^\d+]", "", cfg["telephone"])
        links.append(f'<a class="btn btn-alt" href="tel:{tel}">{html.escape(cfg["telephone"])}</a>')
    return " ".join(links) or '<a class="btn" href="/contacto/">Contacto</a>'


def nap_block(cfg):
    a = cfg["address"]
    parts = [cfg["name"], a["street"], f'{a["locality"]}, Uruguay', cfg["telephone"]]
    return " · ".join(html.escape(p) for p in parts if not is_todo(p))


def build(strict=False):
    cfg = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    pages = load_pages()
    template = (ROOT / "template.html").read_text(encoding="utf-8")
    today = date.today().isoformat()

    todos = list(find_todos(cfg))
    unreviewed = [str(p["source"]) for p in pages if p.get("medical") and not p.get("reviewed")]

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "static", DIST / "static")

    for page in pages:
        body = page["body"]
        body = body.replace("{{faq}}", render_faq(page.get("faq", [])))
        body = body.replace("{{articles}}", render_articles(pages))
        body = body.replace("{{contact}}", contact_links(cfg))
        body = body.replace("{{nap}}", nap_block(cfg))
        # Gate de seguridad: contenido médico sin revisión no se indexa.
        robots = ("noindex, follow" if page.get("medical") and not page.get("reviewed")
                  else "index, follow, max-snippet:-1, max-image-preview:large")
        reviewed_note = ""
        if page.get("medical"):
            reviewed_note = (f'<p class="reviewed">Escrito y revisado por {html.escape(cfg["name"])}'
                             f' · Última revisión: {page.get("last_reviewed", "pendiente")}</p>')
        out = (template
               .replace("{{lang}}", cfg["lang"])
               .replace("{{title}}", html.escape(page["title"]))
               .replace("{{description}}", html.escape(page["description"]))
               .replace("{{canonical}}", cfg["site_url"] + page["path"])
               .replace("{{robots}}", robots)
               .replace("{{site_name}}", html.escape(cfg["name"]))
               .replace("{{og_image}}", cfg["site_url"] + cfg["image"])
               .replace("{{jsonld}}", json.dumps(page_graph(cfg, page, today),
                                                 ensure_ascii=False, indent=1))
               .replace("{{contact}}", contact_links(cfg))
               .replace("{{nap}}", nap_block(cfg))
               .replace("{{reviewed}}", reviewed_note)
               .replace("{{year}}", str(date.today().year))
               .replace("{{body}}", body))
        target = DIST / page["path"].lstrip("/") / "index.html"
        if page["path"] == "/404/":
            target = DIST / "404.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(out, encoding="utf-8")

    indexable = [p for p in pages if p["path"] != "/404/"
                 and not (p.get("medical") and not p.get("reviewed"))]

    urls = "\n".join(
        f'  <url><loc>{cfg["site_url"]}{p["path"]}</loc>'
        f'<lastmod>{p.get("date_modified", today)}</lastmod></url>' for p in indexable)
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8")

    robots = "\n".join(f"User-agent: {b}\nAllow: /\n" for b in AI_BOTS)
    (DIST / "robots.txt").write_text(
        f"{robots}\nUser-agent: *\nAllow: /\n\nSitemap: {cfg['site_url']}/sitemap.xml\n",
        encoding="utf-8")

    c = clean(cfg)
    a = c.get("address", {})
    llms = [f"# {cfg['name']}", "", f"> {cfg['description']}", "",
            "## Datos verificables",
            f"- Especialidad: {cfg['job_title']}",
            f"- Ubicación: {a['locality'] + ', ' if a.get('locality') else ''}Uruguay",
            *([f"- Teléfono: {c['telephone']}"] if c.get("telephone") else []),
            *(f"- Afiliación: {h['name']}" for h in c.get("hospital_affiliations", [])),
            *(f"- Perfil: {s}" for s in c.get("same_as", [])),
            "", "## Páginas",
            *(f"- [{p['title']}]({cfg['site_url']}{p['path']}): {p['description']}"
              for p in indexable)]
    (DIST / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    (DIST / "CNAME").write_text(cfg["site_url"].split("//")[1] + "\n", encoding="utf-8")

    print(f"OK: {len(pages)} páginas → {DIST}")
    if todos:
        print(f"\n⚠ {len(todos)} campos TODO en config.json (se omiten del schema):")
        print("\n".join(f"  - {t}" for t in todos))
    if unreviewed:
        print(f"\n⚠ {len(unreviewed)} páginas médicas sin revisión (publicadas con noindex):")
        print("\n".join(f"  - {u}" for u in unreviewed))
    if strict and (todos or unreviewed):
        sys.exit("\n--strict: completar TODOs y revisar contenido médico antes de publicar.")


if __name__ == "__main__":
    build(strict="--strict" in sys.argv)
