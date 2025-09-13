import os
import requests
import csv
from dotenv import load_dotenv
import time

load_dotenv()

# Get the API key
API_KEY = os.getenv("POLYGON_API_KEY")
LIMIT = 1000
url = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={API_KEY}"
tickers = []

try:
    response = requests.get(url)
    data = response.json()

    for ticker in data['results']:
        tickers.append(ticker)

    while 'next_url' in data:
        
        time.sleep(3) 
        response = requests.get(data['next_url'] + f'&&apiKey={API_KEY}')
        data = response.json()
        for ticker in data['results']:
            tickers.append(ticker)

except Exception as e:
    print(e)

fieldnames = [
    "active",
    "cik",
    "composite_figi",
    "currency_name",
    "last_updated_utc",
    "locale",
    "market",
    "name",
    "primary_exchange",
    "share_class_figi",
    "ticker",
    "type"
]

output_csv = 'all_tickers.csv'
with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for t in tickers:
        row = {key: t.get(key,'') for key in fieldnames}
        writer.writerow(row)




# import os
# import requests
# import csv
# from dotenv import load_dotenv

# load_dotenv()

# # Get the API key
# API_KEY = os.getenv("POLYGON_API_KEY")
# LIMIT = 1000
# url = f"https://api.polygon.io/v3/reference/options/contracts?order=asc&limit={LIMIT}&sort=ticker&apiKey={API_KEY}"

# # Make a single request
# response = requests.get(url)
# data = response.json()

# tickers = []

# # Check if the request was successful and if 'results' key exists
# if response.status_code == 200 and 'results' in data:
#     tickers.extend(data['results'])

# fieldnames = [
#     'additional_underlyings',
#     'cfi',
#     'contract_type',
#     'correction',
#     'exercise_style',
#     'expiration_date',
#     'primary_exchange',
#     'shares_per_contract',
#     'strike_price',
#     'ticker',
#     'underlying_ticker'
# ]

# output_csv = 'tickers.csv'
# with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     for t in tickers:
#         row = {key: t.get(key,'') for key in fieldnames}
#         writer.writerow(row)

# print(f"Successfully saved {len(tickers)} tickers to {output_csv}")