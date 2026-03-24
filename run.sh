#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

DEFAULT_PORT=8000
PORT="$DEFAULT_PORT"

if [[ $# -gt 0 ]]; then
  case "$1" in
    --port|-p)
      if [[ $# -lt 2 ]]; then
        echo "Invalid or missing port argument."
        echo "Usage: ./run.sh [PORT]"
        echo "       ./run.sh --port PORT"
        echo "       ./run.sh -p PORT"
        exit 1
      fi
      PORT="$2"
      ;;
    *)
      PORT="$1"
      ;;
  esac
fi

if ! [[ "$PORT" =~ ^[0-9]+$ ]] || (( PORT < 1 || PORT > 65535 )); then
  echo "Invalid port: $PORT"
  exit 1
fi

echo "Setting backend port to $PORT"
python - "$PORT" <<'PY'
import json
import sys
from pathlib import Path

port = int(sys.argv[1])
backend_cfg = Path("backend/config.json")
root_cfg = Path("config.json")

backend_data = json.loads(backend_cfg.read_text(encoding="utf-8")) if backend_cfg.exists() else {}
backend_data["port"] = port
backend_data.setdefault("remote", False)
backend_cfg.write_text(json.dumps(backend_data, indent=2), encoding="utf-8")

root_data = json.loads(root_cfg.read_text(encoding="utf-8")) if root_cfg.exists() else {}
root_data["backend_url"] = f"http://127.0.0.1:{port}"
root_cfg.write_text(json.dumps(root_data, indent=2), encoding="utf-8")
PY

source venv/bin/activate
python main.py
