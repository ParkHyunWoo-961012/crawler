import datetime

import scrapy
from allnewscrawler.items import AllnewscrawlerItem

class AllcrawlingSpider(scrapy.Spider):

    name = 'allcrawling'


    def start_requests(self):
        try:
            press_list = [172504, 11, 45,174606,396,21,98009,190,15,33,38,2,200,8,17,49,7,5,3589,129
                          ,90,6,216,139,3,19,35,3572,359,43,157,10,4,47,12,244,310,327,75,98,60,73,189,23,318,134,317,59,131,294,297
                          ,94,219,82,85,77,220] # 다음 cap 들어가야됨
            #비즈니스워치까지
            num_of_days_to_crawl = 1
            num_of_pages_to_crawl = 50

            for cp in press_list:
                for time_delta in range(0, num_of_days_to_crawl):
                    for page in range(1, num_of_pages_to_crawl + 1, 1):
                        reg_date = (datetime.datetime.now()+ datetime.timedelta(days=time_delta)).strftime('%Y%m%d')
                        yield scrapy.Request(
                            url="http://news.daum.net/cp/{0}?page={1}&regDate={2}".format(cp, page, reg_date,meta={'dont_redirect': True,"handle_httpstatus_list": [302]}),
                            callback=self.parse_url)

        except Exception as e:
            pass


    def parse_url(self, response):
        pritn("error")
        try:
            for sel in response.xpath('//*[@id="mArticle"]/div[2]/ul/li/div'):
                yield scrapy.Request(
                    url=sel.xpath('strong[@class="tit_thumb"]/a/@href').extract()[0],
                    callback=self.parse,meta={'dont_redirect': True,"handle_httpstatus_list": [302]})

        except Exception as e:
            pass

    def parse(self, response):
              print("error")
        try:
            item = AllnewscrawlerItem()
            item.initialize('')

            item['id'] = response.url.split("/")[-1]
            item['category'] = response.xpath('//*[@id="kakaoBody"]/text()').get()
            item['title'] = response.xpath('//*[@id="cSub"]/div[1]/h3/text()').get()
            item['content'] = response.xpath(
                '//*[@id="harmonyContainer"]/section/div[contains(@dmcf-ptype, "general")]/text()').getall() \
                + response.xpath(
                '//*[@id="harmonyContainer"]/section/p[contains(@dmcf-ptype, "general")]/text()').getall()
            
            element1 = response.xpath('//*[@id="cSub"]/div[1]/span/span[1][@class="txt_info"]/text()').getall()
            num_date1 = response.xpath('//*[@id="cSub"]/div[1]/span/span[1]/span[@class="num_date"]/text()').get()
            element2 = response.xpath('//*[@id="cSub"]/div[1]/span/span[2][@class="txt_info"]/text()').getall()
            num_date2 = response.xpath('//*[@id="cSub"]/div[1]/span/span[2]/span[@class="num_date"]/text()').get()
            element3 = response.xpath('//*[@id="cSub"]/div[1]/span/span[3][@class="txt_info"]/text()').getall()
            num_date3 = response.xpath('//*[@id="cSub"]/div[1]/span/span[3]/span[@class="num_date"]/text()').get()

            if len(element1) != 0:
                if element1[0][:2] == '입력':
                    item['created_date'] = num_date1
                elif element1[0][:2] == '수정':
                    item['updated_date'] = num_date1
                else:
                    pass

            if len(element2) != 0:
                if element2[0][:2] == '입력':
                    item['created_date'] = num_date2
                elif element2[0][:2] == '수정':
                    item['updated_date'] = num_date2
                else:
                    pass

            if len(element3) != 0:
                if element3[0][:2] == '입력':
                    item['created_date'] = num_date3
                elif element3[0][:2] == '수정':
                    item['updated_date'] = num_date3
                else:
                    pass

            logger.info('[parse_news] : ' + response.url)

        except Exception as e:
            pass

        yield item

