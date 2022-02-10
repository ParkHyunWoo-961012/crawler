import datetime

import scrapy
from allnewscrawler.items import AllnewscrawlerItem


import logging
logger = logging.getLogger('all_crawling')

class AllcrawlingSpider(scrapy.Spider):

    name = 'all_crawling'

    def start_requests(self):
        try:
            press_list = [11, 45, 396, 21, 190, 15, 33, 38, 2, 200, 8, 17, 49, 7, 5, 3589, 129, 90, 6, 216, 139, 3, 19,
                          35, 3272, 359, 43, 157, 10, 4, 47, 12, 244, 310, 327, 75, 98, 60, 73, 189, 23, 318, 317, 134,
                          313, 296, 58, 249, 56, 532, 67, 242, 57, 80, 231, 86, 169, 434, 112, 676, 37, 331, 132, 188,
                          13, 176, 210, 320, 144, 284, 555, 301, 234, 302, 291, 181, 326, 180, 70, 285, 724, 246, 110,
                          321, 214, 119, 287, 293, 226, 85, 297, 94, 219, 82, 294, 278, 306, 163, 261, 59, 260, 165,
                          250, 269, 131, 178, 170, 227, 314, 268, 255, 162, 254, 303, 221, 259, 224, 29, 228, 3437, 256,
                          323, 298, 305, 251, 252, 18, 77, 220, 175, 62, 3130, 14, 68, 3510, 22, 295, 95, 122, 79, 65]

            num_of_days_to_crawl = 1
            num_of_pages_to_crawl = 1000

            for cp in press_list:
                for time_delta in range(0, num_of_days_to_crawl):
                    for page in range(1, num_of_pages_to_crawl + 1, 1):
                        reg_date = (datetime.datetime.now() + datetime.timedelta(days=time_delta)).strftime('%Y%m%d')
                        yield scrapy.Request(
                            url="http://media.daum.net/cp/{0}?page={1}&regDate={2}".format(cp, page, reg_date),
                            callback=self.parse_url)

        except Exception as e:
            logger.error('[start_requests] error occurred')
            logger.error(str(e))

    def parse_url(self, response):
        try:
            for sel in response.xpath('//*[@id="mArticle"]/div[2]/ul/li/div'):
                yield scrapy.Request(
                    url=sel.xpath('strong[@class="tit_thumb"]/a/@href').extract()[0],
                    callback=self.parse)

        except Exception as e:
            logger.error('[parse_url] error occurred')
            logger.error(str(e))

    def parse(self, response):
        try:
            item = AllnewscrawlerItem()
            item.initialize('')

            item['id'] = response.url.split("/")[-1]
            item['link'] = response.xpath('//*[@id="cSub"]/div[1]/em/a/img/@alt').get()
            item['category'] = response.xpath('//*[@id="kakaoBody"]/text()').get()
            item['title'] = response.xpath('//*[@id="cSub"]/div[1]/h3/text()').get()
            item['article'] = response.xpath(
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
                    item['editor'] = element1[0]

            if len(element2) != 0:
                if element2[0][:2] == '입력':
                    item['created_date'] = num_date2
                elif element2[0][:2] == '수정':
                    item['updated_date'] = num_date2
                else:
                    item['editor'] = element2[0]

            if len(element3) != 0:
                if element3[0][:2] == '입력':
                    item['created_date'] = num_date3
                elif element3[0][:2] == '수정':
                    item['updated_date'] = num_date3
                else:
                    item['editor'] = element3[0]

            logger.info('[parse_news] : ' + response.url)

        except Exception as e:
            logger.error('[parse_news] error occurred')
            logger.error(str(e))

        yield item
