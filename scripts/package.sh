#!/usr/bin/env bash
# Build dist/masshire-projects-v<version>.zip in the same layout as the
# upload zip: .claude-plugin/plugin.json + skills/.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/validate.py
version=$(python3 -c 'import json;print(json.load(open(".claude-plugin/plugin.json"))["version"])')
out="dist/masshire-projects-v${version}.zip"
mkdir -p dist
rm -f "$out"
zip -qr -X "$out" .claude-plugin/plugin.json skills -x '*.DS_Store'
echo "Built $out"
