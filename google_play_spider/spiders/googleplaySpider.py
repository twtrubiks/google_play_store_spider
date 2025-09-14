# -*- coding: utf-8 -*-
from google_play_spider.items import GooglePlaySpiderItem
import scrapy

class GooglePlaySpider(scrapy.Spider):
      name = "playspider"
      start_urls = [
          "https://play.google.com/store/apps",  # 主頁面
          "https://play.google.com/store/games",  # 遊戲分類
      ]

      def parse(self, response):
          """
          解析起始頁面，找出應用程式連結

          @url https://play.google.com/store/apps
          @returns requests 0 50
          """
          # 取得應用程式連結
          app_links = response.css('a[href*="/store/apps/details"]::attr(href)').getall()

          if not app_links:
              # 如果沒有找到連結，嘗試其他選擇器
              app_links = response.xpath('//a[contains(@href, "/store/apps/details")]/@href').getall()

          self.logger.info(f"找到 {len(app_links)} 個應用程式連結")

          # 限制抓取數量，先測試前 50 個
          for link in app_links[:50]:
              if link:
                  full_url = response.urljoin(link)
                  yield scrapy.Request(full_url, callback=self.parse_app)


      def parse_app(self, response):
          """
          解析單個應用程式頁面

          @returns items 1
          @scrapes title price autor description
          """
          # 使用 CSS 選擇器提取資料
          playitem = GooglePlaySpiderItem()

          # 標題
          title = response.css('h1[itemprop="name"] span::text').get()
          if not title:
              title = response.css('h1 span::text').get()

          # 開發者
          autor = response.css('div.Vbfug a span::text').get()
          if not autor:
              autor = response.css('a[href*="/store/apps/dev"] span::text').get()

          # 價格
          price = response.css('button[aria-label*="Buy"] span::text').get()
          if not price:
              price = response.css('button[aria-label*="Install"]::text').get()
              if price and 'Install' in price:
                  price = 'Free'
          if not price:
              price = 'Free'

          # 評分
          star_rating = response.css('div[role="img"][aria-label*="star"]::attr(aria-label)').get()
          if not star_rating:
              star_rating = response.css('div.TT9eCd::text').get()
          if not star_rating:
              star_rating = 'No rating'

          # 描述
          description_texts = response.xpath('//div[@data-g-id="description"]//text()').getall()
          if description_texts:
              description = ' '.join(description_texts).strip()
          else:
              description = ''

          # 圖片 URL
          img_url = response.css('img[alt*="Icon"][src*="play-lh.googleusercontent.com"]::attr(src)').get()
          if not img_url:
              img_url = response.css('img[itemprop="image"]::attr(src)').get()

          # 開發者 URL
          autor_url = response.css('div.Vbfug a::attr(href)').get()
          if autor_url:
              autor_url = response.urljoin(autor_url)
          else:
              autor_url = ''

          # 分類（從 URL 或頁面中提取）
          category = response.css('a[itemprop="genre"]::text').get()
          if not category:
              category = 'Apps'

          # 填充 Item
          playitem['title'] = title.strip() if title else 'Unknown'
          playitem['title_URL'] = response.url
          playitem['imgURL'] = img_url if img_url else ''
          playitem['description'] = description[:500] if description else ''  # 限制描述長度
          playitem['autor'] = autor.strip() if autor else 'Unknown'
          playitem['autor_URL'] = autor_url
          playitem['star_rates'] = star_rating.strip() if star_rating else 'No rating'
          playitem['price'] = price.strip() if price else 'Free'
          playitem['table_title'] = category.strip() if category else 'Apps'

          yield playitem


