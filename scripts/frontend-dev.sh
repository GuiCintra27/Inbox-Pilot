#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
FRONTEND_DIR="$ROOT_DIR/frontend"
PORT="${PORT:-3000}"

if ! python3 - <<'PY' "$PORT"
import socket
import sys

port = int(sys.argv[1])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    sock.bind(("0.0.0.0", port))
except OSError:
    raise SystemExit(1)
finally:
    sock.close()
PY
then
  echo "Porta $PORT já está em uso."
  echo "Feche o processo atual nessa porta antes de subir o frontend."
  echo "Isso evita o Next mudar silenciosamente para outra porta e confundir o acesso no navegador."
  echo
  lsof -iTCP:"$PORT" -sTCP:LISTEN -n -P || true
  exit 1
fi

python3 - <<'PY' "$FRONTEND_DIR"
from pathlib import Path
import shutil
import sys

frontend_dir = Path(sys.argv[1]).resolve()
next_dir = frontend_dir / ".next"

if not next_dir.exists():
    raise SystemExit(0)

marker = next_dir / "types" / "app" / "layout.ts"
if not marker.exists():
    raise SystemExit(0)

first_line = marker.read_text(encoding="utf-8", errors="ignore").splitlines()[0].strip()
prefix = "// File: "

if not first_line.startswith(prefix):
    raise SystemExit(0)

cached_file = Path(first_line.removeprefix(prefix)).resolve()
cached_frontend_dir = cached_file.parents[2] if len(cached_file.parents) >= 3 else None

if cached_frontend_dir and cached_frontend_dir != frontend_dir:
    shutil.rmtree(next_dir, ignore_errors=True)
    print(
        f"Limpando cache .next incompatível: {cached_frontend_dir} -> {frontend_dir}",
        flush=True,
    )
PY

cd "$FRONTEND_DIR"
exec npm run dev -- --hostname 0.0.0.0 --port "$PORT"
