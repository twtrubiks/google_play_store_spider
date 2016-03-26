#coding=utf8
from google_play_spider.items import GooglePlaySpiderItem
import scrapy

class PttSpider(scrapy.Spider):
      name = "playspider"      
      start_urls = ["https://play.google.com/store/apps/top",
                    "https://play.google.com/store/apps/new"] 

      def parse(self, response):  
          #取得 顯示更多內容 URL
          for url in response.xpath('//a[@class="see-more play-button small id-track-click apps id-responsive-see-more"]'):
              targetURL = "https://play.google.com" + url.xpath('@href')[0].extract()
              #使用POST , 抓資料 100 筆
              yield  scrapy.FormRequest(               
                     targetURL,
                     formdata = {'start':'0',
                                 'num':'100',
                                 'numChildren':'0',
                                 'cctcss':'square-cover',
                                 'cllayout':'NORMAL',
                                 'ipf':'1',
                                 'xhr':'1',
                                 'token':'zNTXc17yBEzmbkMlpt4eKj14YOo:1458833715345'},
                    callback = self.parse_data
                 )


      def parse_data(self, response):  
          #抓取各項資料 使用xpath時,如要抓取一層內的一層,請一層一層往下抓,不要用跳的,不然會抓不到
          playitem = GooglePlaySpiderItem()
          table_title = response.xpath('//div[@class="cluster-heading"]/h2/text()')[0].extract().strip()
          for object_per in response.xpath('//div[@class="card no-rationale square-cover apps small"]/div[@class="card-content id-track-click id-track-impression"]'):
             title = object_per.xpath('div[@class="details"]/a[@class="title"]/text()')[0].extract()
             #print 'title:',title
             title_URL = 'https://play.google.com' + object_per.xpath('div[@class="details"]/a/@href')[0].extract()
             #print 'targrt_URL:',title_URL
             imgURL = 'https:' + object_per.xpath('div[@class="cover"]/div/div/div/img/@data-cover-large')[0].extract()
             #print 'imgURL:', imgURL
             description_list = object_per.xpath('div[@class="details"]/div[@class="description"]/text()')[0].extract()
             description = ''.join(description_list)
             #print 'description',description
             autor = object_per.xpath('div[@class="details"]/div[@class="subtitle-container"]/a/text()')[0].extract()
             #print 'autor:', autor
             autor_URL = 'https://play.google.com' + object_per.xpath('div[@class="details"]/div[@class="subtitle-container"]/a/@href')[0].extract()
             #print 'autor_URL:', autor_URL
             try:
               star = object_per.xpath('div[@class="reason-set"]/span/a/div/div/@aria-label')[0].extract()
             except:
               star = 'no star_rate'
             star_rates = star
             #print 'star rates:',star_rates
             price = object_per.xpath('div[@class="details"]/div[@class="subtitle-container"]/span/span[2]/button/span/text()')[0].extract()
             #print 'price:', price
             #print '================================================='

             playitem['title'] = title.strip()
             playitem['title_URL'] = title_URL.strip()
             playitem['imgURL'] = imgURL.strip()
             playitem['description'] = description.strip()
             playitem['autor'] = autor.strip()
             playitem['autor_URL'] = autor_URL.strip()
             playitem['star_rates'] = star_rates.strip()
             playitem['price'] = price.strip()
             playitem['table_title']= table_title.strip()
             yield playitem
            

