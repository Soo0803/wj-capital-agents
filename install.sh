#!/usr/bin/env bash
# WJ Capital — one-step setup for the wj-finance MCP server.
#
# Safe to re-run: it repairs a broken or half-built venv rather than failing.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"
MCP_DIR="wj-capital/mcp"
VENV="$MCP_DIR/.venv"

bold() { printf '\033[1m%s\033[0m\n' "$1"; }
warn() { printf '\033[33m%s\033[0m\n' "$1"; }
fail() { printf '\033[31m%s\033[0m\n' "$1" >&2; exit 1; }

[ -f "$MCP_DIR/finance_server.py" ] || fail \
  "Run this from the repository root — $MCP_DIR/finance_server.py not found."

# ---------------------------------------------------------------- 1. Python
bold "1/3  Checking Python"
PY=""
for c in python3.13 python3.12 python3.11 python3.10 python3; do
  command -v "$c" >/dev/null 2>&1 || continue
  # 3.10+ is required: the mcp package needs modern typing features.
  if "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)' 2>/dev/null; then
    PY="$c"; break
  fi
done
[ -n "$PY" ] || fail "Python 3.10 or newer is required. Found none on PATH."
echo "     using $PY ($("$PY" --version 2>&1))"

# ---------------------------------------------------------------- 2. venv
bold "2/3  Building the virtualenv"
# A venv, not a bare pip install: Homebrew and Debian Pythons refuse to install
# into the system interpreter (PEP 668), and .mcp.json invokes this exact path.
if [ -x "$VENV/bin/python" ]; then
  echo "     reusing $VENV"
else
  rm -rf "$VENV"
  "$PY" -m venv "$VENV"
  echo "     created $VENV"
fi
"$VENV/bin/python" -m pip install --quiet --upgrade pip
"$VENV/bin/python" -m pip install --quiet -r "$MCP_DIR/requirements.txt"
echo "     dependencies installed"

# ---------------------------------------------------------------- 3. identity
bold "3/3  Checking your SEC EDGAR identity"
UA="${SEC_EDGAR_USER_AGENT:-}"
if [[ "$UA" == *"@"* ]]; then
  echo "     SEC_EDGAR_USER_AGENT = $UA"
  # Prove the server actually starts under the real configuration.
  if "$VENV/bin/python" "$MCP_DIR/finance_server.py" </dev/null >/dev/null 2>&1; then
    echo "     server starts cleanly"
  else
    warn "     server did not start — run it directly to see the error:"
    warn "       $VENV/bin/python $MCP_DIR/finance_server.py"
    exit 1
  fi
  bold "Done. Restart Claude Code."
else
  cat <<'MSG'

  SEC_EDGAR_USER_AGENT is not set, and the server will refuse to start
  without it. SEC EDGAR requires every request to name a real person with a
  reachable email, and it throttles and blocks by identity rather than by IP —
  so this has to be yours, and must not be a shared or invented value.

  Add to ~/.zshrc (or ~/.bashrc), then restart your terminal:

      export SEC_EDGAR_USER_AGENT="Your Name you@example.com"

  Then re-run ./install.sh to verify, and restart Claude Code.

MSG
  exit 1
fi
