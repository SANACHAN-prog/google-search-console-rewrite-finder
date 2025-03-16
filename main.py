#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from GoogleAPIClientWrapper import *
from SearchReportWriter import *

API_SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
API_MAX_ROWS = 1000
API_KEY_FILE = 'key_file.json'

SITE_URL = 'https://progzakki.sanachan.com/'
PERIOD_DAYS = 90

OUTPUT_FILE_CSV = 'page_query_mapping.csv'
OUTPUT_FILE_EXCEL = 'page_query_mapping.xlsx'

def main():
    # 期間の設定
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=PERIOD_DAYS)).strftime('%Y-%m-%d')

    # APIサービスの初期化
    gapi = GoogleAPIClientWrapper(API_KEY_FILE, API_SCOPES, API_MAX_ROWS)

    # データ取得
    df = gapi.fetch_url_query_data(SITE_URL, start_date, end_date)
    print("データの取得が完了しました。")

    # CSVとして保存
    #df.to_csv(OUTPUT_FILE_CSV, index=False, encoding='utf-8')
    #print("データをCSVファイルに出力しました。")

    # Excelとして保存
    writer = SearchReportWriter(OUTPUT_FILE_EXCEL)
    writer.save_to_excel(df)
    print("データをExcelファイルに出力しました。")

if __name__ == "__main__":
    main()

