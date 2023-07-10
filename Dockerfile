# Base image
FROM python:3.9

# Çalışma dizini oluştur
WORKDIR /app

# Gereksinimleri kopyala ve yükle
COPY requirements.txt .
RUN pip install -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Chromium yüklemesi
RUN apt-get update && apt-get install -y chromium

# Playwright gereksinimlerini yükle
RUN playwright install

# Çalıştırma komutu
CMD [ "python", "main.py" ]
