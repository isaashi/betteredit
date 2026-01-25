#!/usr/bin/env bash
set -euo pipefail

# If a virtualenv is active, deactivate it to avoid conflicts
if [ -n "${VIRTUAL_ENV-}" ]; then
  echo "Detected active virtual environment at $VIRTUAL_ENV, deactivating..."
  if declare -f deactivate > /dev/null; then
    deactivate
  else
    echo "Warning: deactivate function not found; please deactivate manually if needed."
  fi
fi

if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "Created virtual environment 'venv'."
else
  echo "Virtual environment 'venv' already exists."
fi

venv/bin/pip install --upgrade pip setuptools wheel
venv/bin/pip install --disable-pip-version-check -r requirements.txt

echo ""
echo "Setup complete"
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
