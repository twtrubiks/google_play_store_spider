# google_play_store_spider

抓取 google play store 資料  use Scrapy on python

* [Demo Video](https://youtu.be/oOSefZYGvf8) - Linux

## 特色

* 抓取 google play store 資料

## 輸出格式  JSON  and DATABASE

```
    "table_title": 標題,
	"title": APP名稱,
	"title_URL": APP網址,
	"imgURL": APP圖片網址
    "description": APP描述,
	"autor": 作者或團隊,
	"autor_URL": 作者或團隊的網址,
    "star_rates": 使用者評分(星星數),
    "price": 免費或價錢,
```

## 使用方法

在路徑底下任何一個資料夾輸入

```
scrapy crawl playspider
```

## 執行過程

![alt tag](http://i.imgur.com/Akrj7IY.jpg)

![alt tag](http://i.imgur.com/YcoqVCs.jpg)

## 輸出畫面

輸出檔案會儲存在 `output/` 目錄下：

- `output/googleplay.json` - JSON 格式的爬取資料

- `output/googleplay.db` - SQLite 資料庫檔案

![alt tag](http://i.imgur.com/2wd59bB.jpg)

googleplay.json

![alt tag](http://i.imgur.com/vFTX3id.jpg)

googleplay.db

![alt tag](http://i.imgur.com/ggGTmJw.jpg)

可以輸入SQLITE指令，搜尋指定的項目

```sql
SELECT * FROM googleplay  WHERE table_title LIKE '遊戲類熱門付費下載'
```

![alt tag](http://i.imgur.com/EuTE3bC.jpg)

## 執行環境

* Python 3.13
* Scrapy 2.13.3

## 技術說明

### ItemAdapter 的使用

本專案使用 Scrapy 2.0+ 引入的 `ItemAdapter` 來處理資料項目。

`ItemAdapter` 提供統一的介面來處理不同類型的 items，讓程式碼更靈活。

在 `pipelines.py` 中的使用範例：

```python
from itemadapter import ItemAdapter

adapter = ItemAdapter(item)
# 獲取所有欄位名稱
col = ','.join(adapter.field_names())
# 獲取所有值
values = list(adapter.values())
# 轉換為字典格式（用於 JSON 輸出）
data = adapter.asdict()
```

### 資料處理流程

```
items.py (定義結構)
    ↓
Spider (創建並填充 Item)
    ↓
Pipeline (用 ItemAdapter 處理)
    ↓
輸出 (JSON/SQLite)
```

### ItemAdapter 重點特性

- **自動識別欄位**：自動讀取 `GooglePlaySpiderItem` 類別中定義的所有 `scrapy.Field()`

- **欄位順序注意**：`field_names()` 返回的是字母排序，需要固定順序以確保資料庫正確對應

- **動態處理**：在 `items.py` 新增或刪除欄位時，ItemAdapter 會自動適應，不需修改 Pipeline 程式碼

- **型別無關**：不只能處理 Scrapy Item，也能處理普通字典、dataclass 等多種資料型別

`ItemAdapter` 是 Scrapy 的依賴套件，會隨 Scrapy 自動安裝，無需額外安裝。

## 注意事項與限制

### 動態內容限制

* Google Play Store 使用大量 JavaScript 動態載入內容

* 目前的爬蟲只能抓取初始載入的靜態內容（約 50-100 個應用程式）

* 無法自動載入「顯示更多」後的內容

### 解決方案

如需抓取更多資料，可考慮以下方案：

* 使用 **Scrapy-Playwright** 來執行 JavaScrip
t
* 分析並直接呼叫 Google Play 的 API endpoints

* 調整爬取策略，從不同分類頁面收集資料

### 爬取速度設定

專案已優化爬取速度設定（見 `settings.py`）：

* `DOWNLOAD_DELAY = 0.2` - 請求間隔 0.2 秒

* `CONCURRENT_REQUESTS = 16` - 並發請求數

* 啟用 AutoThrottle 自動調節速度

請根據實際需求調整這些參數，避免對伺服器造成過大負擔。

## License

MIT license
