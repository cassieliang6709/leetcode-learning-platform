#!/bin/bash
# Install language runtimes into the self-hosted Piston container.
# Run this ONCE after first `docker compose up`.
#
# Usage: bash scripts/setup_piston.sh

set -e

PISTON_URL="http://localhost:2000"

echo "Waiting for Piston to be ready..."
until curl -sf "$PISTON_URL/api/v2/runtimes" > /dev/null; do
  sleep 2
done
echo "Piston is ready."

echo ""
echo "Installing language runtimes..."

install_runtime() {
  local lang=$1
  local version=$2
  echo "  Installing $lang $version..."
  curl -sf -X POST "$PISTON_URL/api/v2/packages" \
    -H "Content-Type: application/json" \
    -d "{\"language\": \"$lang\", \"version\": \"$version\"}" \
    | python3 -c "import sys,json; r=json.load(sys.stdin); print('  OK:', r.get('language'), r.get('language_version',''))" \
    || echo "  WARNING: failed to install $lang $version"
}

# Core languages for AlgoMentor
install_runtime "python"     "3.10.0"
install_runtime "javascript" "18.15.0"
install_runtime "java"       "15.0.2"
install_runtime "cpp"        "10.2.0"
install_runtime "go"         "1.16.2"
install_runtime "rust"       "1.50.0"

echo ""
echo "Done! Installed runtimes:"
curl -sf "$PISTON_URL/api/v2/runtimes" | python3 -m json.tool | grep '"language"'
