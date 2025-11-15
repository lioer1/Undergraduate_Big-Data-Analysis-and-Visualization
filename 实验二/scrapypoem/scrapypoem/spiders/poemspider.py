import scrapy
from scrapy import Request, FormRequest
from scrapypoem.items import ScrapypoemItem


class PoemspiderSpider(scrapy.Spider):
    name = 'poemspider'
    allowed_domains = ['gushiwen.cn']
    start_urls = ['http://www.gushiwen.cn/mingjus/']

    # allowed_domains = ['beijing.8684.cn']
    # search_url = 'http://beijing.8684.cn'

    # # 获得并构建一级网页URL
    # def start_requests(self):
    #     for page in range(9):
    #         url = '{url}/list{page}'.format(url=self.search_url, page=(page + 1))
    #         yield FormRequest(url, callback=self.parse_index)
    #
    # def parse_index(self, response):
    #     print('hello')

    def parse(self, response):
        # 先获每句名句的div
        for box in response.xpath('//div[@class="left"]/div[@class="sons"]'):
            # 获取每句名句的链接
            url = 'https://www.gushiwen.cn' + box.xpath('.//@href').get()
            # 获取每句名句内容
            sentence = box.xpath('.//a[1]/text()').get()
            # 获取每句名句出处
            source = box.xpath('.//a[2]/text()').get()
            # 实例化容器
            item = ScrapypoemItem()
            # # 将收集到的信息封装起来
            item['url'] = url
            item['sentence'] = sentence
            item['source'] = source
            # 处理子页
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_detail)
        # 翻页
        next = response.xpath('//a[@class="amore"]/@href').get()
        if next is not None:
            next_url = 'https://www.gushiwen.cn' + next
            # 处理下一页内容
            yield Request(next_url)

    def parse_detail(self, response):
        # 获取名句的详细信息
        item = response.meta['item']
        content_list = response.xpath('//div[@class="contson"]//text()').getall()
        content = "".join(content_list).strip().replace('\n', '').replace('\u3000', '')
        item['content'] = content
        yield item
# import scrapy
# from scrapypoem.items import ScrapypoemItem
# from scrapy import Request, FormRequest
#
# class PoemspiderSpider(scrapy.Spider):
#     name = 'poemspider'
#     allowed_domains = ['www.gushiwen.cn']
#     start_urls = ['https://www.gushiwen.cn/mingjus/']
#
#     # custom_settings = {
#     #     'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     #     'LOG_LEVEL': 'DEBUG'  # 设置日志级别为 DEBUG，方便调试
#     # }
#
#     def parse(self, response):
#         # 获取每句名句的 div
#         for box in response.xpath('//div[@class="left"]/div[@class="sons"]'):
#             # 获取每句名句的链接
#             url = 'https://www.gushiwen.cn' + box.xpath('.//a[@target="_blank"]/@href').get()
#             # 获取每句名句内容
#             sentence = box.xpath('.//a[1]/text()').get()
#             sentence = box.xpath('.//a[@target="_blank"]/text()').get().strip()
#             # 获取每句名句出处
#             # source = box.xpath('.//a[@target="_blank"]/a/text()').get()
#             source = box.xpath('.//a[2]/text()').get()
#             # if source is None:
#             #     source = box.xpath('.//a[@target="_blank"]/text()').get()
#             # 实例化容器
#             item = ScrapypoemItem()
#             # 将收集到的信息封装起来
#             item['url'] = url
#             item['sentence'] = sentence
#             item['source'] = source.strip() if source else ''
#             # 处理子页
#             yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_detail)
#
#         # 翻页
#         next_page = response.xpath('//a[contains(text(), "下一页")]/@href').get()
#         if next_page is not None:
#             next_url = 'https://www.gushiwen.cn' + next_page
#             # 处理下一页内容
#             yield Request(next_url)
#
#     def parse_detail(self, response):
#         # 获取名句的详细信息
#         item = response.meta['item']
#         content_list = response.xpath('//div[@class="sons"]').getall()
#         content = "".join(content_list).strip().replace('\n', '').replace('\u3000', '')
#         # 提取主要内容部分
#         content = ''.join(response.xpath('//div[@class="contson"]//text()').getall()).strip().replace('\n', '').replace(
#             '\u3000', '')
#         item['content'] = content
#         yield item