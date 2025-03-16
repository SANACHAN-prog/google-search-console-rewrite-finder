#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import unicodedata

from openpyxl import load_workbook
from openpyxl.styles import Alignment

def get_east_asian_width(text):
    """
    文字列の表示幅を計算する
    全角文字は2、半角文字は1として計算
    """
    width = 0
    for c in str(text):
        # East Asian Width (EA)の判定
        if unicodedata.east_asian_width(c) in ['F', 'W', 'A']:
            width += 2
        else:
            width += 1
    return width

class SearchReportWriter:
    def __init__(self, output_file):
        """初期化"""
        self.output_file = output_file

    def __format_search_data(self, df):
        """検索データの整形とリライト推奨の判定"""
        df_sorted = df.sort_values('URL')
        formatted_data = []

        for _, row in df_sorted.iterrows():
            formatted_row = self.__create_formatted_row(row)
            formatted_data.append(formatted_row)

        return pd.DataFrame(formatted_data)

    def __create_formatted_row(self, row):
        """1行分のデータを整形"""
        ctr_value = float(row['CTR'].strip('%'))
        position_value = float(row['掲載順位'])

        return {
            'クエリ': row['クエリ'],
            'URL': row['URL'],
            'クリック数': row['クリック数'],
            '表示回数': row['表示回数'],
            'CTR': row['CTR'],
            '掲載順位': row['掲載順位'],
            'リライト推奨': self.__check_rewrite_recommendation(
                position_value, row['表示回数'], ctr_value)
        }

    def __check_rewrite_recommendation(self, position, impressions, ctr):
        """リライト推奨の判定"""
        return '＊' if (position <= 10 and 
                       impressions >= 100 and 
                       ctr < 3.0) else ''

    def __adjust_column_widths(self, worksheet, df):
        """列幅の調整"""
        for idx, col in enumerate(worksheet.columns):
            max_length = get_east_asian_width(df.columns[idx])
            column = col[0].column_letter

            for cell in col:
                try:
                    width = get_east_asian_width(cell.value)
                    if width > max_length:
                        max_length = width
                except:
                    pass

            worksheet.column_dimensions[column].width = (max_length + 2)

    def __set_cell_alignments(self, worksheet, df):
        """セルの配置設定"""
        for idx, col in enumerate(worksheet.columns):
            if df.columns[idx] in ['CTR', '掲載順位']:
                for cell in col:
                    cell.alignment = Alignment(horizontal='right')

    def save_to_excel(self, df):
        """Excelファイルとして保存"""
        formatted_df = self.__format_search_data(df)

        with pd.ExcelWriter(self.output_file, engine='openpyxl') as writer:
            formatted_df.to_excel(writer, index=False, sheet_name='検索データ')
            worksheet = writer.sheets['検索データ']

            self.__adjust_column_widths(worksheet, formatted_df)
            self.__set_cell_alignments(worksheet, formatted_df)
