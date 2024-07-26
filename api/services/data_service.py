import requests
import json
import os
from dotenv import load_dotenv
from api.services.auth_service import token_required

# Load the .env file
load_dotenv()

# Retrieve the necessary values from the .env file
gatewayUri = os.getenv('GATEWAY_URI')
endpoint = os.getenv('ENDPOINT')


def fetch_data():
    sql_query = input("SQL sorgusunu girin: ")
    query = sql_query
    url = gatewayUri + endpoint
    response = send_query(url, query)

    if response.status_code == 200:
        data = response.json()
        # Etiketleri kontrol et
        if check_json_labels(data):
            return data
        else:
            raise ValueError("Eksik etiketler mevcut.")
    else:
        raise ValueError(f"Bir hata oluştu: {response.status_code} - {response.text}")


def send_query(url, query):
    # Dönüştürülmüş sorguyu belirtilen URL'ye gönderir.
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(query))
    return response


def check_json_labels(data):
    required_labels = {"Date", "Product Id", "InputStockCount", "OutputStockCount", "Stock"}

    if "data" in data:
        for entry in data["data"]:
            if not required_labels.issubset(entry.keys()):
                print(f"Eksik etiketler: {required_labels - entry.keys()} at entry {entry}")
                return False
        print("Tüm gerekli etiketler mevcut.")
        return True
    else:
        print("JSON yapısında 'data' anahtarı bulunamadı.")
        return False