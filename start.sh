#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
	echo "Erro: uv não está instalado. Instale com: pip install uv"
	exit 1
fi

echo "Instalando/sincronizando dependências com uv..."
uv sync

echo "Iniciando FastAPI em modo dev..."
uv run fastapi dev main.py
