FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /URL-Shortener

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt gunicorn

COPY . .

EXPOSE 80

CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:80 --workers 1 url_shortener.wsgi:application"]
