#!/usr/bin/env bash
# Lance la présentation HTML d'un cours dans le navigateur par défaut.
#
# Usage :
#   ./scripts/present.sh CM1_Fondamentaux_architecture

set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

NAME="${1:-CM1_Fondamentaux_architecture}"
HTML_FILE="$ROOT_DIR/export/${NAME}.html"

if [ ! -f "$HTML_FILE" ]; then
  echo "Fichier $HTML_FILE introuvable, génération via export_slides.sh…"
  "$ROOT_DIR/scripts/export_slides.sh"
fi

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$HTML_FILE" >/dev/null 2>&1 &
else
  echo "Ouvre manuellement le fichier dans ton navigateur :"
  echo "  $HTML_FILE"
fi
