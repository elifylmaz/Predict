import requests
import json
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Retrieve the necessary values from the .env file
gatewayUri = os.getenv('GATEWAY_URI')
firm_number = os.getenv('FIRM_NUMBER')
section_number = os.getenv('SECTION_NUMBER')
endpoint = os.getenv('ENDPOINT')
def fetch_data():

    url = gatewayUri + endpoint

    # Format the FIRM_NUMBER to a 3-digit format (e.g., 003)
    formatted_firm_number = f"{int(firm_number):03}"
    formatted_section_number = f"{int(section_number):02}"

    query = '''
    SELECT

    [Date]=STLINE.DATE_,
    [Product Id]=ITEM.LOGICALREF,
    [InputStockCount]= 
    ISNULL((SELECT SUM(ST.AMOUNT) FROM LG_{firm_number}_{section_number}_STLINE ST WHERE ST.STOCKREF=ITEM.LOGICALREF AND ST.IOCODE=1 AND ST.DATE_=STLINE.DATE_),0),
    [OutputStockCount]= 
    ISNULL((SELECT SUM(ST.AMOUNT) FROM LG_{firm_number}_{section_number}_STLINE ST WHERE ST.STOCKREF=ITEM.LOGICALREF AND ST.IOCODE=4 AND ST.DATE_=STLINE.DATE_),0),
    [Stock]=
    ISNULL((SELECT SUM(TOT.ONHAND) FROM LV_{firm_number}_{section_number}_STINVTOT TOT WHERE TOT.STOCKREF=ITEM.LOGICALREF AND TOT.DATE_=STLINE.DATE_ AND TOT.INVENNO <> -1),0)



    FROM
    LG_{firm_number}_{section_number}_STLINE STLINE 
    LEFT JOIN LG_{firm_number}_ITEMS ITEM ON ITEM.LOGICALREF=STLINE.STOCKREF
    GROUP BY STLINE.DATE_,ITEM.LOGICALREF
    ORDER BY ITEM.LOGICALREF DESC
        '''

    # Insert formatted_firm_number into the query
    query = query.format(firm_number=formatted_firm_number, section_number=formatted_section_number)
    # Convert query to JSON format
    body = json.dumps(query)
    headers = {'Content-Type': 'application/json'}

    # Send POST request to the API
    response = requests.post(url, data=body, headers=headers)

    try:
        data = response.json()
    except ValueError:
        data = response.text

    return data