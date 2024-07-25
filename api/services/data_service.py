import requests
import json
import os
from dotenv import load_dotenv

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
    # JSON verilerini dosyaya kaydet
    save_to_json(response)

def send_query(url, query):

    #Dönüştürülmüş sorguyu belirtilen URL'ye gönderir.
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(query))
    return response

def save_to_json(response):
    if response.status_code == 200:
        # JSON veriyi al
        data = response.json()
        # JSON veriyi dosyaya yaz
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print("Veriler data.json dosyasına kaydedildi.")
        # Etiketleri kontrol et
        check_json_labels('data.json')
    else:
        print(f"Bir hata oluştu: {response.status_code} - {response.text}")


def check_json_labels(file_path):
    required_labels = {"Date", "Product Id", "InputStockCount", "OutputStockCount", "Stock"}
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)

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


# fetch_data fonksiyonunu çağırarak işlemi başlatabilirsiniz.
fetch_data()