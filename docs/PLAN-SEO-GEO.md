# Plan SEO + GEO drcorujo.uy — versión corregida

Estado al 24-10-2026. Objetivo: que Google y los LLMs (ChatGPT, Gemini, Perplexity, Claude) reconozcan y citen al Dr. Federico Corujo como cirujano de cataratas en Uruguay, con **< 2 h/mes de tu tiempo** después del setup.

---

## 0. Diagnóstico (lo que el plan original no vio)

| Hallazgo | Impacto |
|---|---|
| **drcorujo.uy no resuelve en DNS** (ENOTFOUND al 24-10-2026) | Bloqueante. No hay nada que auditar ni que indexar. Las Fases 1-2 del plan original asumían un sitio existente. |
| La entidad "Federico Corujo oftalmólogo" **no aparece** en búsqueda web; lo único indexado es LinkedIn (figura en San José, no Montevideo). | Para los LLMs hoy no existís como entidad médica. El problema no es optimizar, es **crear la entidad**. |
| El apellido colisiona con Mathías Corujo (futbolista). | Desambiguación obligatoria: usar siempre "Dr. Federico Corujo, oftalmólogo" + schema con `sameAs`. |
| Ciudad inconsistente (LinkedIn: San José / plan: Montevideo). | Rompe el NAP. Definir **una** dirección principal y replicarla igual en todos lados. |

## 1. Críticas al plan original

1. **Herramientas antes que entidad.** "seoagents" y "NotFair" no son verificables como MCPs establecidos; instalar paquetes pip desconocidos con Playwright en tu máquina es riesgo de supply chain sin retorno claro. **Descartados.** Claude Code + este repo hacen lo mismo sin dependencias.
2. **Antigravity + licencia**: costo sin necesidad para un sitio de 10 páginas. Descartado.
3. **Backlinks "dofollow" por outreach**: bajo apalancamiento para un médico local. Lo que mueve la aguja: Google Business Profile, reseñas, directorios médicos, prensa y tu producción académica (PubMed/ORCID).
4. **"¿Quién es el mejor oftalmólogo…?"**: sirve como pregunta de medición, **nunca** como copy. El Código de Ética Médica (Ley 19.286) y el Colegio Médico restringen publicidad comparativa y testimonios. Nada de "el mejor", "garantizado", ni resultados prometidos.
5. **FAQPage**: desde 2023 Google casi no muestra rich results de FAQ para sitios no institucionales. Se mantiene igual porque los LLMs sí extraen bien ese formato, pero no esperes estrellitas en Google.
6. **"+40 % de visibilidad en IA"**: viene de un paper académico (GEO, Princeton 2023) en condiciones de laboratorio. Usar como principio (citas + datos + fuentes), no como promesa.
7. **Test manual de 20 preguntas × 4 motores × cada mes** = ~3 h/mes de tu tiempo. **Automatizado** (ver §4).
8. **Schema**: `Physician` a secas está desactualizado; schema.org tiene `IndividualPhysician` para médicos individuales. Implementado como grafo `Person` ↔ `IndividualPhysician` ↔ `WebSite`.
9. Faltaba: `llms.txt`, permitir explícitamente crawlers de IA en `robots.txt`, gate de revisión médica, y desambiguación de nombre.

## 2. Qué quedó implementado en este repo

| Pieza | Archivo | Qué hace |
|---|---|---|
| Fuente única NAP/entidad | `site/config.json` | Un solo lugar para nombre, dirección, teléfono, afiliaciones, perfiles. Todo el schema sale de acá. |
| Generador estático | `site/build.py` | HTML puro, sin JS, Core Web Vitals máximos. Genera JSON-LD, `sitemap.xml`, `robots.txt`, `llms.txt`, `CNAME`. |
| Gate de seguridad médica | front matter `"reviewed": false` | Toda página médica sin tu revisión sale con `noindex` y fuera del sitemap/llms.txt. `--strict` bloquea si hay TODOs. |
| Páginas "answer-first" | `site/pages/` | Inicio, Sobre mí, Cirugía de cataratas, FAQ (8), Contacto, Artículos + 1er artículo (recuperación). Cada H2 es una pregunta + TL;DR. |
| Schema | automático | `WebSite`, `Person`, `IndividualPhysician`, `MedicalWebPage`, `MedicalProcedure`, `FAQPage`, `Article`, `BreadcrumbList`. |
| Deploy | `.github/workflows/deploy.yml` | GitHub Pages, gratis, en cada push a `main`. |
| Monitor GEO | `geo-monitor/` + workflow mensual | Pregunta 15 consultas de pacientes a Claude con búsqueda web geolocalizada en Uruguay, registra menciones y URLs citadas en `results/AAAA-MM.csv`. |

## 3. Plan de ejecución (ordenado por apalancamiento)

### Semana 1 — Existir (tu tiempo: ~2 h; resto delegable a secretaria)
1. **Dominio/DNS** (15 min): verificar registro de drcorujo.uy en NIC.uy (Antel). Apuntar DNS a GitHub Pages: registros `A` a 185.199.108.153 / .109 / .110 / .111 y `CNAME www → fedecorujo.github.io`. En el repo: Settings → Pages → Source: GitHub Actions, custom domain `drcorujo.uy`, Enforce HTTPS.
2. **Completar `site/config.json`** (30 min): todos los `TODO`. Elegir **una** dirección principal.
3. **Foto profesional** → `site/static/dr-corujo.jpg` (1200×1200, < 200 KB).
4. **Revisar contenido médico** (45 min): leer las 3 páginas médicas, ajustar a tu protocolo, completar los `TODO` del HTML, poner `"reviewed": true` y `"last_reviewed": "AAAA-MM-DD"`.
5. **Google Business Profile** (delegable): categoría principal "Oftalmólogo", NAP idéntico a `config.json`, horarios, 10 fotos reales, enlace a drcorujo.uy. Pegar la URL del perfil en `same_as`.
6. **Google Search Console + Bing Webmaster** (10 min): verificar dominio por DNS, enviar `sitemap.xml`. Bing importa: alimenta a ChatGPT/Copilot.

### Semanas 2-4 — Consolidar la entidad (delegable al 80 %)
7. **Perfiles con NAP idéntico** (secretaria, checklist): Doctoralia UY, LinkedIn (actualizar ciudad y titular "Médico oftalmólogo · Cirujano de cataratas", enlazar web), ORCID, Google Scholar, Sociedad de Oftalmología del Uruguay, páginas de staff de las instituciones donde operás (pedir que enlacen a drcorujo.uy — **es el backlink de mayor valor**).
8. **Sistema de reseñas**: QR/link de reseña de Google entregado en el control posoperatorio de 1 semana (no en el día de la cirugía). Meta: 20 reseñas en 90 días. Sin incentivos (prohibido por Google).
9. **Wikidata** (30 min, alto apalancamiento): crear ítem "Federico Corujo" (ocupación: oftalmólogo, país: Uruguay, ORCID, web oficial). Los LLMs usan Wikidata para resolver entidades. Solo hechos verificables.

### Mes 2-6 — Contenido citable (1 artículo cada 2 semanas, ~20 min tuyos c/u)
10. **Pipeline de contenido automatizado**: dictás 5 min de audio con tu respuesta clínica → Claude Code lo convierte en artículo con la estructura del template (`site/pages/articulos/`) → revisás → `reviewed: true` → push. Publicación automática.
11. Backlog priorizado por intención de paciente:
    - LASIK vs PRK vs lentes fáquicos (si lo hacés)
    - Lente monofocal vs multifocal vs EDOF: cuál elegir
    - Cataratas y manejo nocturno
    - Opacificación capsular y láser YAG
    - Cataratas en pacientes diabéticos
    - Deporte después de cirugía ocular (pádel, remo, náutica — tu diferencial auténtico)
12. **Dato propio en cada artículo** (casuística, tiempos promedio de tu práctica). Es lo que un LLM no puede obtener de otra fuente → motivo para citarte.
13. **YouTube/LinkedIn**: reutilizar el mismo audio/video. Descripción = TL;DR + link. No producir contenido aparte.

### Continuo — PR y autoridad
14. **Prensa**: 1 pitch por trimestre a El País / El Observador / la diaria / Montevideo Portal sobre temas de agenda (miopía infantil y pantallas, Día Mundial de la Visión – 2º jueves de octubre). Ofrecerte como fuente. 1 mención en medio nacional > 50 backlinks de directorios.
15. **Académico**: cada publicación/charla en congreso → entrada en "Sobre mí" + ORCID. Señal E-E-A-T de máxima calidad.

## 4. Medición (automatizada)

- **Mensual, automático**: `geo-monitor` corre el día 1, guarda CSV en el repo. Requiere secreto `ANTHROPIC_API_KEY` en Settings → Secrets → Actions. Costo estimado: < USD 3/mes.
- **Manual mínimo** (trimestral, 15 min): las 5 preguntas de marca en ChatGPT, Gemini y Perplexity. Agregar sus APIs al monitor es el siguiente paso si el canal muestra tracción.
- **Search Console**: revisión mensual de impresiones/consultas. Pedirle a Claude Code: *"Analizá el export de Search Console y el último CSV de geo-monitor: ¿qué preguntas tienen impresiones sin citación en IA y qué artículo falta?"*

### KPIs a 6 meses
| KPI | Línea base | Meta |
|---|---|---|
| Sitio indexado (páginas en Google) | 0 | 100 % del sitemap |
| Knowledge panel / perfil GBP con reseñas | no | sí, ≥ 20 reseñas ≥ 4.8 |
| Menciones en geo-monitor (preguntas de marca) | 0/5 | 5/5 |
| Menciones en geo-monitor (preguntas genéricas Uruguay) | 0/10 | ≥ 3/10 |
| Consultas originadas en web/GBP por mes | ? (medir con "¿cómo nos conoció?") | definir tras mes 1 |

## 5. Lo que necesito de vos (decisiones, no tareas)
1. Dirección principal: ¿Montevideo o San José? ¿Una o dos sedes? (Si dos: agrego `PhysiciansOffice` por sede.)
2. ¿Qué lentes intraoculares y procedimientos ofrecés realmente? (Define backlog de contenido.)
3. ¿Querés publicar precios orientativos? ("¿Cuánto cuesta…?" es una de las consultas más frecuentes a LLMs.)
4. ¿Merge de este branch a `main` para activar el deploy?
