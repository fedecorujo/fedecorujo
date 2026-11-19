#!/bin/bash
# Espeja el repo drcorujo dentro del vault de Obsidian (iCloud) en <vault>/DrCorujo/.
# - docs, marketing, bases, plantillas, 00-Inicio: se sobrescriben (fuente = repo).
# - contenido/: solo se agregan notas nuevas; tus cambios de estado en el vault se respetan.
# - privado/: nunca se toca (vive solo en iCloud, no en GitHub).
# Uso: tools/sync-to-vault.sh "/ruta/al/vault"   (o variable VAULT)
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
VAULT="${1:-${VAULT:-}}"
[ -n "$VAULT" ] && [ -d "$VAULT" ] || { echo "Vault no encontrado: '$VAULT'" >&2; exit 1; }
DEST="$VAULT/DrCorujo"
mkdir -p "$DEST/privado/pacientes" "$DEST/privado/derivadores"

git -C "$REPO" pull --ff-only --quiet || echo "Aviso: git pull falló, se usa la copia local." >&2

for d in docs marketing plantillas; do
  rsync -a --delete "$REPO/$d/" "$DEST/$d/"
done
cp "$REPO/00-Inicio.md" "$DEST/00-Inicio DrCorujo.md"
rsync -a --ignore-existing "$REPO/contenido/" "$DEST/contenido/"

# Bases: las rutas pasan a ser relativas a DrCorujo/ dentro del vault.
mkdir -p "$DEST/bases"
for f in "$REPO"/bases/*.base; do
  sed 's/inFolder("/inFolder("DrCorujo\//' "$f" > "$DEST/bases/$(basename "$f")"
done
echo "OK $(date '+%F %T') → $DEST"
