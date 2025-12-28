# 圖片轉 WebP 工具 (Image to WebP Converter)

這是一個簡單的 Python GUI 應用程式，可以批次將圖片資料夾中的檔案轉換為 `.webp` 格式。

## 功能
- 選擇輸入資料夾 (支援 jpg, png, bmp, tiff 等)
- 選擇輸出資料夾
- 批次轉換並顯示進度

## 安裝與執行

### 前置需求
- Python 3.x

### 安裝依賴
由專案根目錄執行：

```bash
# Windows
python -m venv venv
venv\Scripts\pip install -r requirements.txt
```

### 執行程式
方式一 (推薦)：
直接雙擊 `start.bat` 檔案。

方式二 (手動)：
```bash
venv\Scripts\python converter.py
```

## 使用方法
1. 執行應用程式。
2. 點擊「瀏覽」選擇包含圖片的**輸入資料夾**。
3. 點擊「瀏覽」選擇存放結果的**輸出資料夾**。
4. 點擊「開始轉換」。
