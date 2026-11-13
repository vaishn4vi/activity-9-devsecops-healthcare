FROM python:3.12-slim

RUN apt-get update && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=5000
WORKDIR /app
RUN groupadd --system appgroup && useradd --system --gid appgroup --home-dir /app appuser
COPY requirements.txt .
RUN pip install --no-cache-dir --no-compile -r requirements.txt
COPY app.py .
COPY templates ./templates
COPY static ./static
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=2)"
CMD ["python", "app.py"]
