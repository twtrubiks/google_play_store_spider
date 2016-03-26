# google_play_store_spider
抓取 google play store 資料  use Scrapy on python
* [Demo Video](https://youtu.be/oOSefZYGvf8) - Linux 

## 特色
* 抓取 google play store 資料 (熱門排行榜 最新發佈) 前100筆資料
   
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
路徑底下會多出兩個檔案  googleplay.json 、googleplay.db <br>
![alt tag](http://i.imgur.com/2wd59bB.jpg)
googleplay.json<br>
![alt tag](http://i.imgur.com/vFTX3id.jpg)
googleplay.db<br>
![alt tag](http://i.imgur.com/ggGTmJw.jpg)

可以輸入SQLITE指令，搜尋指定的項目
```
SELECT * FROM googleplay  WHERE table_title LIKE '遊戲類熱門付費下載'

```
![alt tag](http://i.imgur.com/EuTE3bC.jpg)

## 執行環境
* Ubuntu 12.04
* Python 2.7.3
* Scrapy 1.0.4

## License
MIT license

