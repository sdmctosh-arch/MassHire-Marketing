#!/usr/bin/env bash
# Build dist/<plugin>-v<version>.zip for each plugin (or only those named as
# arguments), in the same layout as the upload zips:
# .claude-plugin/plugin.json + skills/.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/validate.py
mkdir -p dist
names=("$@")
[ ${#names[@]} -eq 0 ] && names=($(ls plugins))
for name in "${names[@]}"; do
  dir="plugins/$name"
  [ -d "$dir" ] || { echo "No plugin $dir" >&2; exit 1; }
  version=$(python3 -c "import json;print(json.load(open('$dir/.claude-plugin/plugin.json'))['version'])")
  out="$PWD/dist/${name}-v${version}.zip"
  rm -f "$out"
  (cd "$dir" && zip -qr -X "$out" .claude-plugin/plugin.json skills -x '*.DS_Store')
  echo "Built dist/${name}-v${version}.zip"
done
