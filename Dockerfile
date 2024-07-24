# Temel Python imajını kullanın
FROM python:3.9

# Çalışma dizinini oluşturun ve ayarlayın
WORKDIR /app

# Gereksinim dosyalarını konteyner içine kopyalayın
COPY requirements.txt /app/

# Bağımlılıkları yükleyin
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını konteyner içine kopyalayın
COPY . /app

# .env dosyasını konteynerin kök dizinine kopyalayın
COPY .env /app/.env

# PYTHONPATH çevre değişkenini ayarlayın
ENV PYTHONPATH=/app

# API uygulamasını çalıştırın
CMD ["python", "api/app.py","--host","0.0.0.0","--port","5000"]
