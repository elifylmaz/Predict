import requests
import json

def send_query(url, query):

    #Dönüştürülmüş sorguyu belirtilen URL'ye gönderir.
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(query))
    return response


def main():
    sql_query = input("SQL sorgusunu girin: ") #"SELECT [Date]=STLINE.DATE_,[Product Id]=ITEM.LOGICALREF, [InputStockCount]=ISNULL((SELECT SUM(ST.AMOUNT) FROM LG_003_01_STLINE ST WHERE ST.STOCKREF=ITEM.LOGICALREF AND ST.IOCODE=1 AND ST.DATE_=STLINE.DATE_), 0), [OutputStockCount]=ISNULL((SELECT SUM(ST.AMOUNT) FROM LG_003_01_STLINE ST WHERE ST.STOCKREF=ITEM.LOGICALREF AND ST.IOCODE=4 AND ST.DATE_=STLINE.DATE_), 0), [Stock]=ISNULL((SELECT SUM(TOT.ONHAND) FROM LV_003_01_STINVTOT TOT WHERE TOT.STOCKREF=ITEM.LOGICALREF AND TOT.DATE_=STLINE.DATE_ AND TOT.INVENNO <> -1), 0) FROM LG_003_01_STLINE STLINE LEFT JOIN LG_003_ITEMS ITEM ON ITEM.LOGICALREF=STLINE.STOCKREF GROUP BY STLINE.DATE_, ITEM.LOGICALREF ORDER BY ITEM.LOGICALREF DESC"
    query = sql_query
    url = "http://172.25.86.101:1234/gateway/customQuery/CustomQuery"
    response = send_query(url, query)

    print("HTTP Durum Kodu:", response.status_code)
    print("Yanıt İçeriği:", response.text)


if __name__ == "__main__":
    main()
