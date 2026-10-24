# drcorujo.uy

Sitio del Dr. Federico Corujo, oftalmólogo (Uruguay). Estático, sin dependencias, optimizado para buscadores y motores de IA (SEO + GEO).

- Plan y roadmap: [`docs/PLAN-SEO-GEO.md`](docs/PLAN-SEO-GEO.md)
- Captación de cirugías (auditoría, estrategia, KPIs): [`docs/MARKETING-CATARATAS.md`](docs/MARKETING-CATARATAS.md) · kits operativos en [`marketing/`](marketing/)
- Obsidian: abrir el repo como vault → `00-Inicio.md` (ver `docs/OBSIDIAN.md`)
- Skills de Claude Code: `/contenido-paciente`, `/responder-resena`, `/reporte-captacion` (`.claude/skills/`)
- Importar contenido del sitio actual: `python3 site/import_existing.py https://drcorujo.uy`
- Datos de la entidad (NAP, perfiles): [`site/config.json`](site/config.json)
- Páginas: `site/pages/` (front matter JSON + HTML)
- Monitor de citaciones en IA: [`geo-monitor/`](geo-monitor/)

## Uso

```bash
python3 site/build.py           # genera dist/ y lista TODOs pendientes
python3 site/build.py --strict  # falla si hay TODOs o contenido médico sin revisar
python3 -m http.server -d dist  # vista previa en http://localhost:8000
```

Las páginas con `"medical": true` se publican con `noindex` hasta tener `"reviewed": true`.
Push a `main` → deploy automático a GitHub Pages.
