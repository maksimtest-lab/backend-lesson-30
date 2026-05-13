FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    netcat-openbsd \
    postgresql-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8333", "--workers", "4", "--threads", "2"]
