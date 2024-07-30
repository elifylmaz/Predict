
FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY .env /app/.env

ENV PYTHONPATH=/app

CMD ["python", "api/app.py","--host","0.0.0.0","--port","5000"]
