# -*- coding: utf-8 -*-
import re
import scrapy
from urllib.parse import urlencode
from scrapy.http import Request
from recruit.items import RecruitItem

# scrapy crawl zhilian -a input_keyword=python -a input_page=1 -s COLLECTION=python -s set_mongo=1


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['sou.zhaopin.com', 'jobs.zhaopin.com']
    start_urls = ['http://sou.zhaopin.com/']

    def __init__(self, input_keyword, input_page,input_area, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = input_keyword
        self.input_page = int(input_page)
        if self.input_page>10:
            self.input_page=10
        self.area=input_area

        print('self.keyword>>>>>>>>>>>',self.keyword)

    def start_requests(self):
        data = {
            'jl': 489,#默认为全国
            'kw': self.keyword,
            'kt': 3
        }
        base_url = 'http://sou.zhaopin.com/?'
        for page in range(self.input_page):
            data['p'] = page+1
            data['jl']=self.area
            self.url = base_url+urlencode(data)
            print('self.url>>>>>>>>>>>>>>>>>>>>>', self.url)
            yield Request(url=self.url, callback=self.parse)

    def parse(self, response):

        if response.status == 200:
            results = response.xpath(
                '//*[@id="listContent"]/div[contains(@class,"conten")]')
            for result in results[:3]:
                re_url = result.xpath('div/a/@href').get()
                yield Request(url=re_url, callback=self.re_parse)

    def re_parse(self, response):

        if response.status == 200:
            item = RecruitItem()

            item['url'] = response.url
            item['keyword'] = self.keyword
            # 职位：str
            item['position'] = response.xpath(
                '//*[@id="root"]/div[3]/div/div/h3/text()').get()
            # 月薪：str
            item['monthly_pay_range'] = response.xpath(
                '//div[contains(@class,"summary-plane__left")]/span[contains(@class,"summary-plane__salary")]/text()').get()

            item['monthly_pay_min'] = re.findall('\d+\.?\d*',response.xpath('//div[contains(@class,"summary-plane__left")]/span[contains(@class,"summary-plane__salary")]/text()').get())[0]

            item['monthly_pay_max'] = re.findall('\d+\.?\d*',response.xpath('//div[contains(@class,"summary-plane__left")]/span[contains(@class,"summary-plane__salary")]/text()').get())[1]

            # 公司名字：str
            item['company_name'] = response.xpath(
                '//div[contains(@class,"company")]/a/text()').get()
            # 地点：str
            item['site'] = response.xpath(
                '//ul[contains(@class,"summary-plane__info")]/li/text()').get()
            # 经验：str
            item['experience'] = response.xpath(
                '//ul[contains(@class,"summary-plane__info")]/li/text()').getall()[-3]
            # 教育背景：str
            item['education_background'] = response.xpath(
                '//ul[contains(@class,"summary-plane__info")]/li/text()').getall()[-2]
            # 招聘人数：str
            item['number_of_people'] = response.xpath(
                '//ul[contains(@class,"summary-plane__info")]/li/text()').getall()[-1]
            # 职位亮点：strline
            item['bright_spots'] = ','.join(response.xpath(
                '//div[contains(@class,"highlights")]/div/span/text()').getall())
            # 职位信息：strline
            item['position_information'] = ''.join(response.xpath('//div[contains(@class,"describtion__detail-content")]//text()').getall())
            # 公司该概况：str
            item['company_profile'] = response.xpath(
                '//div[contains(@class,"company")]/div[contains(@class,"company__description")]/text()').get()

            yield item
