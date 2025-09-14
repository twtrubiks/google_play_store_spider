# Output Directory

這個目錄用於儲存所有爬蟲的輸出檔案。

## 檔案說明

- `googleplay.json` - JSON 格式的爬取資料
- `googleplay.db` - SQLite 資料庫檔案

## 注意事項

1. 這個目錄已被加入 `.gitignore`，不會被提交到版本控制
2. 每次執行爬蟲時，檔案會被覆蓋
3. 如需保留歷史資料，請手動備份或修改程式碼加入時間戳記

## 查看資料

### JSON 檔案

```bash
cat output/googleplay.json | jq '.'
```

### SQLite 資料庫

```bash
sqlite3 output/googleplay.db "SELECT * FROM googleplay LIMIT 5;"
```

## 清理輸出

```bash
rm -f output/*
```
