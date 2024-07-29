import requests
import json
import os
from dotenv import load_dotenv
from flask import request

# Load the .env file
load_dotenv()

# Retrieve the necessary values from the .env file
gatewayUri = os.getenv('GATEWAY_URI')
endpoint = os.getenv('ENDPOINT')

def fetch_data():
    # Ham JSON verisini al
    raw_data = request.data.decode('utf-8')  # bytes to string
    print("Gelen ham JSON verisi:", raw_data)
    print("Gelen ham JSON verisinin tipi:", type(raw_data))

    try:
        # JSON stringini doğrudan SQL sorgusu olarak al
        sql_query = json.loads(raw_data)
        print("Dönüştürülmüş SQL sorgusu:", sql_query)
        print("SQL sorgusunun tipi:", type(sql_query))
    except json.JSONDecodeError:
        raise ValueError("JSON verisi çözülürken bir hata oluştu.")

    # URL ve diğer ayarları yapılandır
    url = gatewayUri + endpoint
    response = send_query(url, sql_query)

    if response.status_code == 200:
        data = response.json()
        if check_json_labels(data):
            return data
        else:
            raise ValueError("Eksik etiketler mevcut.")
    else:
        raise ValueError(f"Bir hata oluştu: {response.status_code} - {response.text}")

def send_query(url, query):
    headers = {'Content-Type': 'application/json'}
    # SQL sorgusunu JSON nesnesi içinde göndermek
    response = requests.post(url, headers=headers, json=query)
    return response

def check_json_labels(data):
    required_labels = {"Date", "Product Id", "InputStockCount", "OutputStockCount", "Stock"}

    if "data" in data:
        for entry in data["data"]:
            if not required_labels.issubset(entry.keys()):
                print(f"Eksik etiketler: {required_labels - set(entry.keys())} at entry {entry}")
                return False
        print("Tüm gerekli etiketler mevcut.")
        return True
    else:
        print("JSON yapısında 'data' anahtarı bulunamadı.")
        return False
