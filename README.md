# 圖片轉 WebP 工具 (Image to WebP Converter)

這是一個簡單的 Python GUI 應用程式，可以批次將圖片資料夾中的檔案轉換為 `.webp` 格式。

## 為什麼選擇 WebP？ (Why WebP?)

WebP 是一種現代圖片格式，由 Google 開發，旨在為網頁提供更優異的無損和有損壓縮。

### WebP vs JPG vs PNG
| 特性 | WebP | JPG (JPEG) | PNG |
| :--- | :--- | :--- | :--- |
| **檔案大小** | 🏆 極小 (通常比 JPG 小 25-34%，比 PNG 小 26%) | 小 | 大 |
| **有損壓縮** | ✅ 支援 | ✅ 支援 (主要模式) | ❌ 不支援 |
| **無損壓縮** | ✅ 支援 | ❌ 不支援 | ✅ 支援 (主要模式) |
| **透明背景 (Alpha)** | ✅ 支援 (即使是有損模式) | ❌ 不支援 | ✅ 支援 |
| **動畫** | ✅ 支援 | ❌ 不支援 (需用 MJPEG) | ❌ 不支援 (需用 APNG) |

### 適用環境
- **網站開發**：大幅減少網頁載入時間，提升 SEO 分數 (Core Web Vitals)。
- **App 開發**：減少 App 安裝包體積 (APK/IPA size) 及運行時記憶體佔用。
- **存儲空間優化**：備份照片時可節省大量硬碟空間。

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
