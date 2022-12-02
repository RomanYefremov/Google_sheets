import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pycoingecko import CoinGeckoAPI
import time

while True:
    cg = CoinGeckoAPI()

    dict1 = ['ariva', 'axel', 'berry', 'bitcci-cash', 'bitcoinz', 'edain', 'equilibrium', 'amber',
             'empire-token', 'fio-protocol', 'gas', 'gulfcoin-2', 'hoge-finance', 'hzm-coin',
             'intexcoin', 'kala', 'kleekai', 'metaverse-face', 'malinka', 'merchant-token', 'nuco-cloud',
             'ovato', 'plc-ultima', 'pointpay', 'soloxcoin', 'safemoon-inu', 'taboo-token',
             'tcgcoin-2-0', 'the-last-war', 'united-token', 'vica-token', 'volt-inu-2', 'wingriders', 'xrdoge',
             'mirai-token']
    # инит таблицу и ключи к ней<------------
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'credentials.json')

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # айди таблицы и указания листа<------------
    SAMPLE_SPREADSHEET_ID = 'SheetsID'
    SAMPLE_RANGE_NAME = 'Лист1'

    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()

    result = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                         range=SAMPLE_RANGE_NAME).execute()

    data_from_sheet = result.get('values', [])
    # удаление из двблицы элиментов по заданым координатам в range<------------
    spreadsheet_id = 'SheetsID'
    request = service.clear(spreadsheetId=spreadsheet_id, range='Лист1!F2:I36').execute()
    # цыкл в сбора данных по апи<------------
    for i in dict1:
        h = cg.get_coins_markets(vs_currency='usd', ids=i, price_change_percentage='1h,24h,7d', sparkline=True)
        correntprice = h[0]['current_price']
        pricechange1h = h[0]['price_change_percentage_1h_in_currency']
        pricechange24h = h[0]['price_change_percentage_24h_in_currency']
        pricechange7d = h[0]['price_change_percentage_7d_in_currency']
        name = h[0]['symbol']
        if pricechange1h is None:
            pricechange1h = 0
        if pricechange24h is None:
            pricechange24h = 0
        if pricechange7d is None:
            pricechange7d = 0
        # запись в таблицу<------------
        array = {'values': [[correntprice, round(pricechange1h, 2), round(pricechange24h, 2), round(pricechange7d, 2)]]}
        range_ = 'Лист1!F2:I36'
        response = service.append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                  range=range_,
                                  valueInputOption='USER_ENTERED',
                                  body=array).execute()
    time.sleep(10800)
