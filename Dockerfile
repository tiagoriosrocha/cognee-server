FROM python:3.11-slim

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install minimal build deps (some pip packages may need them)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install (adds gunicorn for production run)
COPY requirements.txt ./
RUN pip install --upgrade pip
# Garantir python-dotenv para que o Flask CLI carregue .flaskenv no runtime
RUN pip install -r requirements.txt python-dotenv gunicorn

# Copy project
COPY . /app

# Expose Flask port configured in app.py
EXPOSE 5001

# Use flask run so o .flaskenv seja considerado (assume que .flaskenv está copiado ou montado em /app)
# Não definimos FLASK_APP aqui para respeitar as variáveis do arquivo .flaskenv
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
