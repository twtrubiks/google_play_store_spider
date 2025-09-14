# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import sqlite3
from pathlib import Path
from itemadapter import ItemAdapter

# 設定輸出目錄
OUTPUT_DIR = Path('output')
OUTPUT_DIR.mkdir(exist_ok=True)  # 確保目錄存在

# 設定輸出檔案路徑
fileName = OUTPUT_DIR / 'googleplay.json'
db = OUTPUT_DIR / 'googleplay.db'

class GooglePlaySpiderPipeline(object):
    def __init__(self):
        # 確保輸出目錄存在
        OUTPUT_DIR.mkdir(exist_ok=True)

        # json
        with open(fileName, 'w', encoding='utf-8') as f:
            f.write('[\n')

        # 定義固定的欄位順序（與資料庫表格一致）
        self.field_order = ['table_title', 'title', 'title_URL', 'imgURL',
                           'description', 'autor', 'autor_URL', 'star_rates', 'price']

    def open_spider(self, spider):
        #sqlite
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.cur.execute('DROP TABLE IF EXISTS googleplay')
        self.cur.execute('create table if not exists googleplay(table_title varchar(20),title varchar(50), title_URL varchar(100), imgURL varchar(100), description varchar(250), autor varchar(30), autor_URL varchar(100), star_rates varchar(20), price varchar(10))')

    def close_spider(self, spider):
        #sqlite
        self.con.commit()
        self.con.close()

        #json
        with open(fileName, 'r') as f:
            content = f.read()
        with open(fileName, 'w') as f:
            f.write( content[:-1] + "\n]" )

    def process_item(self, item, spider):
        # 使用 ItemAdapter 處理 item
        adapter = ItemAdapter(item)

        # sqlite - 使用固定順序插入資料
        col = ','.join(self.field_order)
        placeholders = ','.join(len(self.field_order) * '?')
        values = [adapter.get(field) for field in self.field_order]  # 按照固定順序獲取值
        sql = 'INSERT INTO googleplay({}) values({})'
        self.cur.execute(sql.format(col, placeholders), values)

        # json
        line = json.dumps(adapter.asdict(), ensure_ascii=False, indent=4) + ','
        with open(fileName, 'a', encoding='utf-8') as f:
            f.write(line)
        return item

