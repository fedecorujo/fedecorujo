# Integración con tu second brain (Obsidian + iCloud)

Tu vault ya vive en iCloud y se sincroniza Mac ↔ iPhone. Este repo **no** va dentro de iCloud (iCloud corrompe carpetas `.git`). En su lugar, la Mac espeja el repo dentro del vault, en la carpeta `DrCorujo/`, cada hora.

```
GitHub (repo público) ──git pull──▶ ~/Code/drcorujo ──rsync c/hora──▶ iCloud/<vault>/DrCorujo/ ──iCloud──▶ iPhone
                                                                       └─ privado/  (solo iCloud, nunca GitHub)
```

## Setup (10 min, una vez, en la Mac)
```bash
xcode-select --install                     # git (si no lo tenés)
git clone -b claude/dr-corujo-marketing-strategy-3gjx8k https://github.com/fedecorujo/fedecorujo ~/Code/drcorujo
VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/NOMBRE-DE-TU-VAULT"
~/Code/drcorujo/tools/sync-to-vault.sh "$VAULT"          # primera copia

# Automático cada hora:
sed -e "s|REPO_PATH|$HOME/Code/drcorujo|" -e "s|VAULT_PATH|$VAULT|" \
  ~/Code/drcorujo/tools/uy.drcorujo.vault-sync.plist > ~/Library/LaunchAgents/uy.drcorujo.vault-sync.plist
launchctl load ~/Library/LaunchAgents/uy.drcorujo.vault-sync.plist
```
Reemplazá `NOMBRE-DE-TU-VAULT` (en Finder: iCloud Drive → Obsidian → la carpeta de tu vault). Log: `/tmp/drcorujo-vault-sync.log`.

## Reglas de la carpeta `DrCorujo/` en tu vault
| Carpeta | Quién manda | Si la editás en Obsidian |
|---|---|---|
| `docs/`, `marketing/`, `plantillas/`, `bases/` | Repo (Claude) | Se pisa en la próxima sincronización. Pedí cambios a Claude. |
| `contenido/` | Vos, después de creada | Se respeta. Claude solo agrega notas nuevas. |
| `privado/pacientes`, `privado/derivadores` | Vos | Nunca se toca ni sale de iCloud. |

Abrí `DrCorujo/00-Inicio DrCorujo` y agregalo a tu nota índice del second brain.

## Antigravity
Abrí `~/Code/drcorujo` en Antigravity para trabajar el sitio y los kits; tu second brain lo sigue leyendo como siempre. Mismo resultado con Claude Code local en esa carpeta (usa las skills `/contenido-paciente`, `/reporte-captacion`, `/responder-resena`).
