# 比特幣價格自相關性分析

這個專案用於分析比特幣價格的自相關性，使用 Binance 的 1 分鐘 K 線數據進行分析。

## 功能特點

- 從 Binance 獲取 BTC/USDT 1 分鐘 K 線數據
- 進行時間序列自相關性分析
- 使用 ACF (Auto-Correlation Function) 和 PACF (Partial Auto-Correlation Function) 進行分析
- 視覺化分析結果

## 環境需求

- Python 3.8+
- Conda 環境管理工具

## 安裝

使用 Conda 建立環境：

```bash
# 建立環境
conda env create -f environment.yaml

# 啟動環境
conda activate crypto-analysis

# 更新現有環境
conda env update -f environment.yaml --prune
```

## 使用方法

1. 設定 Binance API 金鑰（如需要）：
   - 在 `config.py` 中設定你的 API 金鑰

2. 運行程式：
```bash
python main.py
```

## 分析結果

程式會輸出：
- ACF 和 PACF 圖表
- 自相關性統計數據
- 時間序列平穩性檢定結果

## 注意事項

- Binance API 有請求頻率限制
- 建議使用 VPN 以避免 IP 被封鎖
- 大量數據分析可能需要較長時間 