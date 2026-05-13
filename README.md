# Задание

- Создайте модели Product, Rating и Comment, где Product будет иметь отношение "один-ко-многим" к Rating и Comment.

- Напишите ModelSerializer для всех трёх моделей. Далее, создайте отдельный Serializer для получения рейтинга товара с его комментариями. В этом Serializer реализуйте метод, который позволит пользователю ввести идентификатор товара, а затем вернет его рейтинг и список всех комментариев, связанных с этим товаром.


⚠️ Важно:
Начиная с Django 4.0, в CSRF_TRUSTED_ORIGINS обязательно должен быть протокол (http://), иначе Django не примет значение.

```python
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8111',
    'http://localhost:8111',
    'http://127.0.0.1:8333',
    'http://localhost:8333',
]
```

## 📌 О проекте

Этот проект представляет собой базовый шаблон для развёртывания Django‑приложения в Docker‑окружении с использованием:

- **Django** — backend‑фреймворк
- **Gunicorn** — WSGI‑сервер
- **Nginx** — reverse‑proxy и отдача статики
- **PostgreSQL** — база данных
- **Docker Compose** — оркестрация сервисов

Архитектура полностью повторяет продакшен‑подход:
отдельные контейнеры для приложения, базы данных и nginx, сборка статики, entrypoint, ожидание БД и т.д.

---

## 🧱 Структура проекта

```
project/
│── backend/
│   ├── config/
│   ├── app/
│   ├── manage.py
│── nginx/
│   └── nginx.conf
│── db/                # данные PostgreSQL (volume)
│── Dockerfile
│── docker-compose.yaml
│── entrypoint.sh
│── README.md
```

---

## 🚀 Запуск проекта

Ниже — пошаговая инструкция по запуску проекта **с нуля**.

## Запуск

```bash
sudo docker compose down
sudo docker compose build --no-cache
sudo docker compose up
```
---

## ⚙️ Переменные окружения

Все параметры БД задаются в `docker-compose.yaml`:

```yaml
environment:
  DB_HOST: db
  DB_PORT: 5432
  DB_NAME: drf
  DB_USER: drf
  DB_PASSWORD: drf
```

---

## 📁 Статика

Django собирает статику в `/app/static`, которая шарится между контейнерами:

```yaml
volumes:
  - static_volume:/app/static
```

Nginx отдаёт её через:

```nginx
location /static/ {
    alias /app/static/;
}
```

---

## 🔐 CSRF Trusted Origins
## Создание суперпользователя
```bash
sudo docker compose exec web python manage.py createsuperuser
```
⚠️ Важно:
Начиная с Django 4.0, в CSRF_TRUSTED_ORIGINS обязательно должен быть протокол (http://), иначе Django не примет значение.

Для корректной работы админки:

```python
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8111',
    'http://localhost:8111',
    'http://127.0.0.1:8333',
    'http://localhost:8333',
]
```

---

## 🗄️ Бэкап базы данных

### Создать дамп:

```bash
docker compose exec db pg_dump -U drf -d drf > backup.sql
```

### Восстановить:

```bash
docker compose exec -T db psql -U drf -d drf < backup.sql
```

---

## 🧹 Полная остановка и очистка

```bash
docker compose down
docker system prune -f
```

---
