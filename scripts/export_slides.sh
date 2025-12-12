#!/usr/bin/env bash
# Exporte tous les cours (cm/*.md) en PDF et HTML via Marp CLI.

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v marp >/dev/null 2>&1; then
  echo "Erreur : la commande 'marp' n'est pas disponible."
  echo "Installe Marp CLI, par exemple :"
  echo "  sudo npm install -g @marp-team/marp-cli"
  exit 1
fi

OUT_DIR="$ROOT_DIR/export"
mkdir -p "$OUT_DIR"

for file in cm/*.md; do
  [ -e "$file" ] || continue
  
  # Exclure les fichiers archivés
  if [[ "$file" == *.archived ]]; then
    echo "Ignorer $file (archived)"
    continue
  fi
  
  base="$(basename "$file" .md)"
  echo "Export de $file -> $OUT_DIR/${base}.pdf / .html"

  marp "$file" --pdf --allow-local-files --output "$OUT_DIR/${base}.pdf"
  marp "$file" --allow-local-files --output "$OUT_DIR/${base}.html"
done

echo "✅ Export terminé. Fichiers disponibles dans : $OUT_DIR"
