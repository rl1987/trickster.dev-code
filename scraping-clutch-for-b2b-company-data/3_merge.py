#!/usr/bin/python3

import sqlite3

import pandas as pd

def main():
    list_df = pd.read_csv('lists.csv')
    list_df = list_df.rename(columns={'company_url': 'url'})
    
    page_df = pd.read_csv('pages.csv')
    
    df = list_df.merge(page_df, on='url')
    del df['region']

    print(df)
    
    df.to_csv('clutch.csv', index=False)
    
    conn = sqlite3.connect('clutch.sqlite3')
    df.to_sql('clutch_listing', conn, index=False)
    conn.close()
    
if __name__ == "__main__":
    main()
    