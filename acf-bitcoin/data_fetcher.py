from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta
import time
import os
import json

class DataFetcher:
    def __init__(self, base_path='data'):
        self.client = Client()
        self.base_path = base_path
        
    def _get_file_path(self, exchange, symbol, interval, date):
        """生成檔案路徑"""
        return os.path.join(
            self.base_path,
            exchange.lower(),
            symbol.lower(),
            interval.lower(),
            f"{date.strftime('%Y-%m-%d')}.csv"
        )
    
    def _fetch_klines(self, symbol, interval, start_time, end_time):
        """從 Binance 獲取 K 線數據"""
        try:
            klines = self.client.get_historical_klines(
                symbol=symbol,
                interval=interval,
                start_str=start_time.strftime('%Y-%m-%d %H:%M:%S'),
                end_str=end_time.strftime('%Y-%m-%d %H:%M:%S')
            )
            
            if not klines:
                return None
                
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
            return df
            
        except Exception as e:
            print(f"獲取數據時發生錯誤: {e}")
            return None
    
    def get_data(self, exchange, symbol, interval, start_date, end_date):
        """
        獲取指定時間範圍的數據
        
        Parameters:
        -----------
        exchange : str
            交易所名稱，例如 'binance'
        symbol : str
            交易對，例如 'BTCUSDT'
        interval : str
            K線間隔，例如 '1m'
        start_date : datetime
            開始日期
        end_date : datetime
            結束日期
        
        Returns:
        --------
        pandas.DataFrame
            合併後的數據
        """
        all_data = []
        current_date = start_date
        
        while current_date <= end_date:
            file_path = self._get_file_path(exchange, symbol, interval, current_date)
            
            # 檢查檔案是否存在
            if os.path.exists(file_path):
                print(f"讀取現有數據: {file_path}")
                df = pd.read_csv(file_path, index_col='timestamp', parse_dates=True)
            else:
                print(f"從 API 獲取數據: {current_date.strftime('%Y-%m-%d')}")
                # 計算當天的開始和結束時間
                day_start = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
                day_end = day_start + timedelta(days=1)
                
                df = self._fetch_klines(symbol, interval, day_start, day_end)
                
                if df is not None and not df.empty:
                    # 確保目錄存在
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    # 儲存數據
                    df.to_csv(file_path)
                    print(f"數據已儲存至: {file_path}")
                
            if df is not None and not df.empty:
                all_data.append(df)
            
            current_date += timedelta(days=1)
            time.sleep(0.5)  # 避免 API 限制
        
        if all_data:
            return pd.concat(all_data)
        return None

def main():
    # 測試代碼
    fetcher = DataFetcher()
    start_date = datetime(2024, 4, 7)
    end_date = datetime(2024, 5, 7)
    
    df = fetcher.get_data(
        exchange='binance',
        symbol='BTCUSDT',
        interval='1m',
        start_date=start_date,
        end_date=end_date
    )
    
    if df is not None:
        print(f"獲取到 {len(df)} 筆數據")
        print("\n數據預覽:")
        print(df.head())
    else:
        print("無法獲取數據")

if __name__ == "__main__":
    main() 