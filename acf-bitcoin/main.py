from data_fetcher import DataFetcher
from arima_analysis import check_stationarity, plot_acf_pacf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def main():
    # 初始化數據獲取器
    fetcher = DataFetcher()
    
    # 設定時間範圍
    start_date = datetime(2024, 5, 1)
    end_date = datetime(2024, 5, 7)
    
    # 獲取數據
    df = fetcher.get_data(
        exchange='binance',
        symbol='BTCUSDT',
        interval='1s',
        start_date=start_date,
        end_date=end_date
    )
    
    if df is None:
        print("無法獲取數據")
        return

    # 準備數據
    timeseries = df['close']
    
    # 檢查平穩性
    stationarity = check_stationarity(timeseries)
    print("\n平穩性檢定結果:")
    print(f"ADF 統計量: {stationarity['ADF Statistic']:.4f}")
    print(f"p-value: {stationarity['p-value']:.4f}")
    print("\n臨界值:")
    for key, value in stationarity['Critical Values'].items():
        print(f"{key}: {value:.4f}")

    # 計算自相關性
    autocorr = pd.Series(timeseries).autocorr()
    print(f"\n一階自相關係數: {autocorr:.4f}")

    # 繪製 ACF 和 PACF 圖
    plot_acf_pacf(timeseries, lags=60)  # 分析前 60 個滯後期

    # 繪製價格走勢圖
    plt.figure(figsize=(12, 6))
    plt.plot(timeseries.index, timeseries, label='BTC 價格')
    plt.title('BTC/USDT 1分鐘價格走勢')
    plt.xlabel('時間')
    plt.ylabel('價格 (USDT)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main() 