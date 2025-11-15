from urllib.parse import urljoin

import scrapy
from scrapy import Spider,FormRequest,Request

from beibus.items import BeibusItem


class BeiBusSpider(scrapy.Spider):
    name = 'bei_bus'
    allowed_domains = ['beijing.8684.cn']
    search_url = 'http://beijing.8684.cn'

    # 获得并构建一级网页URL
    def start_requests(self):
        for page in range(9):
            url = '{url}/list{page}'.format(url=self.search_url, page=(page + 1))
            yield FormRequest(url, callback=self.parse_index)

    # 构建二级网页(公交路线详情页url)
    def parse_index(self, response):
        beijingbus = response.xpath('//div[@class="cc-content"]/div[2]/a/@href').extract()
        for href in beijingbus:
            url2 = urljoin(self.search_url, href)
            yield Request(url2, callback=self.parse_detail)

    # 解析详情页信息提取目标信息
    def parse_detail(self, response):
        # 线路名称
        line_name = response.xpath('//h1[@class="title"]/text()').extract_first()
        # 线路类型
        line_type = response.xpath('//a[@class="category"]/text()').extract_first()
        try:
            # 总里程
            mileage = response.xpath('//div[@class="change-info mb20"]/text()').extract_first()
        except:
            mileage = ""
        # 运行时间
        run_time = response.xpath('//ul[@class="bus-desc"]/li[1]/text()').extract_first()
        # 参考票价
        ticket = response.xpath('//ul[@class="bus-desc"]/li[2]/text()').extract_first()
        # 公交公司
        company = response.xpath('//ul[@class="bus-desc"]/li[3]//text()').extract()[1]
        # 最后更新
        update_last = response.xpath('//ul[@class="bus-desc"]/li[4]/text()').extract_first()

        wang_line_list = []
        fan_line_list = []

        wang_line_name = ""
        fan_line_name = ""

        line_name_list = response.xpath('//div[@class="trip"]/text()')
        if mileage != "":
            wang_line_list = response.xpath('//div[@class="layout-left"]/div[7]/ol/li/a/text()')
        else:
            wang_line_list = response.xpath('//div[@class="layout-left"]/div[6]/ol/li/a/text()')

        wang_line_name = line_name + "(" + line_name_list[0].extract() + ")"

        try:
            if mileage != "":
                fan_line_list = response.xpath('//div[@class="layout-left"]/div[9]/ol/li/a/text()')
            else:
                fan_line_list = response.xpath('//div[@class="layout-left"]/div[8]/ol/li/a/text()')
            fan_line_name = line_name + "(" + line_name_list[1].extract() + ")"
        except:
            fan_line_list = []

        # 公交路线-往(环形线默认为此项)
        wang_info = wang_line_name + "\n"
        # 公交路线-返
        fan_info = fan_line_name + "\n"

        for i in range(len(wang_line_list)):
            if i != (len(wang_line_list) - 1):
                wang_info += wang_line_list[i].extract() + ","
            else:
                wang_info += wang_line_list[i].extract()

        if len(fan_line_list) != 0:
            for i in range(len(fan_line_list)):
                if i != (len(fan_line_list) - 1):
                    fan_info += fan_line_list[i].extract() + ","
                else:
                    fan_info += fan_line_list[i].extract()
        bus_item = BeibusItem()
        for field in bus_item.fields:
            bus_item[field] = eval(field)
        yield bus_item
