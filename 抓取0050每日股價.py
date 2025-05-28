#抓取0050 5月股價
#新版(自己從F12找到API)

import requests
import pandas as pd

def fetch_stock_day(stock_no, date_str):
    url = 'https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY'
    params = {
        'date': date_str, 
        'stockNo': stock_no,
        'response': 'json'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data.get('stat') == 'OK':
        df = pd.DataFrame(data['data'], columns=data['fields'])

        #把民國年轉成西元年
        df['日期'] = df['日期'].apply(lambda x: str(int(x.split('/')[0]) + 1911) + '-' + x.split('/')[1] + '-' + x.split('/')[2])
        df['日期'] = pd.to_datetime(df['日期'])

        return df
    else:
        print("查無資料")
        return pd.DataFrame()

df = fetch_stock_day('0050', '20250502') #因為此API本來就是抓五月整個月的，所以以第一天作為代表
df.to_csv("C:/Users/User/Desktop/0050_5月股價.csv", index=False, encoding='utf-8-sig')




# 抓取0050 1~6月股價
def fetch_stock_six_months(stock_no, year, start_month=1):
    frames = []
    for month in range(start_month, start_month + 6):
        if month > 12:
            # 若跨年度月份從1開始
            y = year + 1
            m = month - 12
        else:
            y = year
            m = month
        date_str = f"{y}{m:02d}01"
        print(f"抓取 {stock_no} {y} 年 {m} 月資料...")
        df_month = fetch_stock_day(stock_no, date_str)
        if not df_month.empty:
            frames.append(df_month)
    if frames:
        return pd.concat(frames, ignore_index=True)
    else:
        return pd.DataFrame()

df = fetch_stock_six_months('0050', 2025, 1)
df.to_csv("C:/Users/User/Desktop/0050_1~6月股價.csv", index=False, encoding='utf-8-sig')





