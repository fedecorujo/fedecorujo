# Obsidian como centro de operaciones

El repositorio **es** el vault. Claude Code (nube o local) edita y hace push; Obsidian hace pull. Sin servicios intermedios.

## Setup (15 min, una vez)
1. Obsidian ≥ 1.9 (trae **Bases**). En la Mac: `git clone https://github.com/fedecorujo/fedecorujo ~/Obsidian/drcorujo` → Obsidian → "Abrir carpeta como vault".
2. Plugin de comunidad **Obsidian Git** → Auto pull cada 10 min, auto commit+push cada 30 min, "Pull on startup". En iPhone/iPad funciona igual (autenticación con token de GitHub).
3. Ajustes → Plantillas → carpeta `plantillas`.
4. Abrir `00-Inicio.md`.

## Qué vive dónde
| Contenido | Dónde | Por qué |
|---|---|---|
| Estrategia, kits, calendario, borradores | Vault → git (público) | Nada sensible; Claude lo edita |
| **Pacientes y derivadores** | Vault → `privado/` (en `.gitignore`) | **El repo es público.** Datos personales nunca a GitHub (Ley 18.331) |
| Pipeline que usa la secretaria | **Notion** (se mantiene) | Obsidian es monousuario; la secretaria necesita acceso compartido y desde el celular |

## Notion → Obsidian
Plugin oficial **Importer** → Notion → exportar desde Notion "Markdown & CSV" → importar a `privado/`. Hacerlo solo si la secretaria deja de usar Notion.

## Claude ↔ Obsidian en tu Mac (opcional, alto apalancamiento)
Correr Claude Code dentro de `~/Obsidian/drcorujo`: lee y escribe todo el vault (incluido `privado/`, que nunca sale de tu máquina) y usa las skills `/contenido-paciente`, `/reporte-captacion`, `/responder-resena`. No hace falta un MCP de Obsidian: Claude Code trabaja directo sobre los archivos.
