#!/usr/bin/env python3
"""Monitor mensual de visibilidad en IA generativa (GEO).

Hace cada pregunta de queries.txt a Claude con búsqueda web (ubicación: Uruguay)
y registra si menciona a la entidad y qué URLs cita. Resultado: results/AAAA-MM.csv

Requiere: pip install anthropic · variable ANTHROPIC_API_KEY.
"""
import csv
import sys
from datetime import date
from pathlib import Path

import anthropic

HERE = Path(__file__).parent
ENTITY_TERMS = ["corujo", "drcorujo.uy"]
DOMAIN = "drcorujo.uy"
MODEL = "claude-opus-5-5"

client = anthropic.Anthropic()


def ask(question):
    messages = [{"role": "user", "content": question}]
    # pause_turn: la búsqueda server-side puede pausar; se reenvía para continuar.
    for _ in range(3):
        response = client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            output_config={"effort": "medium"},
            system="Respondé como un asistente para un paciente en Uruguay. Si recomendás profesionales, nombralos.",
            tools=[{
                "type": "web_search_20260209",
                "name": "web_search",
                "max_uses": 5,
                "user_location": {"type": "approximate", "country": "UY",
                                  "city": "Montevideo", "timezone": "America/Montevideo"},
            }],
            messages=messages,
        )
        if response.stop_reason != "pause_turn":
            break
        messages.append({"role": "assistant", "content": response.content})
    return response


def analyze(response):
    if response.stop_reason == "refusal":
        return "", [], "refusal"
    text = "".join(b.text for b in response.content if b.type == "text")
    cited = []
    for b in response.content:
        if b.type == "text":
            for c in b.citations or []:
                url = getattr(c, "url", None)
                if url and url not in cited:
                    cited.append(url)
    return text, cited, response.stop_reason


def main():
    questions = [q.strip() for q in (HERE / "queries.txt").read_text(encoding="utf-8").splitlines()
                 if q.strip() and not q.startswith("#")]
    out = HERE / "results" / f"{date.today():%Y-%m}.csv"
    out.parent.mkdir(exist_ok=True)
    rows, hits = [], 0
    for q in questions:
        try:
            text, cited, stop = analyze(ask(q))
        except anthropic.APIStatusError as e:
            print(f"ERROR {e.status_code}: {q}", file=sys.stderr)
            continue
        mentioned = any(t in text.lower() for t in ENTITY_TERMS)
        own_cited = any(DOMAIN in u for u in cited)
        hits += mentioned
        rows.append({
            "fecha": date.today().isoformat(), "motor": MODEL, "pregunta": q,
            "menciona": "sí" if mentioned else "no",
            "cita_web_propia": "sí" if own_cited else "no",
            "urls_citadas": " | ".join(cited), "stop": stop,
            "respuesta": text[:1500].replace("\n", " "),
        })
        print(f"[{'✓' if mentioned else '·'}] {q}")
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["fecha"])
        w.writeheader()
        w.writerows(rows)
    print(f"\nMenciones: {hits}/{len(rows)} → {out}")


if __name__ == "__main__":
    main()
