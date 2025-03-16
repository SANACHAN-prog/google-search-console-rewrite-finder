#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pandas as pd

from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleAPIClientWrapper():
    def __init__(self, key_file_path, scopes, row_limit):
        """Search Console APIのサービスを初期化"""
        self.__credentials = service_account.Credentials.from_service_account_file(
            key_file_path,
            scopes=scopes
        )
        self.__service = build('searchconsole', 'v1', credentials=self.__credentials)
        self.__row_limit = row_limit

    def fetch_url_query_data(self, site_url, start_date, end_date):
        """URLとクエリの関連データを取得"""
        request = {
            'startDate': start_date,
            'endDate': end_date,
            'dimensions': ['page', 'query'],
            'rowLimit': self.__row_limit,
            'startRow': 0,
            # クリック数で降順ソート
            'orderBy': [
                {
                    'fieldName': 'clicks',      # clicks/impressions/ctr/position
                    'sortOrder': 'DESCENDING'   # ASCENDING/DESCENDING
                }
            ]
        }

        response = self.__service.searchanalytics().query(
            siteUrl=site_url,
            body=request
        ).execute()

        rows = []
        if 'rows' in response:
            for row in response['rows']:
                rows.append({
                    'URL': row['keys'][0],
                    'クエリ': row['keys'][1],
                    'クリック数': row['clicks'],
                    '表示回数': row['impressions'],
                    'CTR': f"{(row['ctr'] * 100):.2f}%",
                    '掲載順位': f"{row['position']:.2f}"
                })

        return pd.DataFrame(rows)
