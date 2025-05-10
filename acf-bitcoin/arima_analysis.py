import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

def check_stationarity(timeseries):
    """
    檢查時間序列的平穩性
    
    Parameters:
    -----------
    timeseries : pandas.Series
        時間序列數據
    
    Returns:
    --------
    dict
        包含 ADF 檢定結果的字典
    """
    result = adfuller(timeseries.dropna())
    return {
        'ADF Statistic': result[0],
        'p-value': result[1],
        'Critical Values': result[4]
    }

def plot_acf_pacf(timeseries, lags=40):
    """
    繪製 ACF 和 PACF 圖
    
    Parameters:
    -----------
    timeseries : pandas.Series
        時間序列數據
    lags : int
        滯後期數
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    plot_acf(timeseries, ax=ax1, lags=lags)
    plot_pacf(timeseries, ax=ax2, lags=lags)
    plt.tight_layout()
    plt.show()

def fit_arima(timeseries, order):
    """
    擬合 ARIMA 模型
    
    Parameters:
    -----------
    timeseries : pandas.Series
        時間序列數據
    order : tuple
        (p, d, q) 參數
    
    Returns:
    --------
    statsmodels.tsa.arima.model.ARIMAResults
        ARIMA 模型結果
    """
    model = ARIMA(timeseries, order=order)
    results = model.fit()
    return results

def forecast_arima(model, steps=30):
    """
    使用 ARIMA 模型進行預測
    
    Parameters:
    -----------
    model : statsmodels.tsa.arima.model.ARIMAResults
        ARIMA 模型結果
    steps : int
        預測步數
    
    Returns:
    --------
    pandas.Series
        預測結果
    """
    forecast = model.forecast(steps=steps)
    return forecast 