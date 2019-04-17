# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecruitItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    keyword = scrapy.Field()

    position = scrapy.Field()#职位               
    monthly_pay_range = scrapy.Field()#月薪
    monthly_pay_min = scrapy.Field()
    monthly_pay_max = scrapy.Field()
    company_name = scrapy.Field()#公司名字
    site = scrapy.Field()#地点
    experience = scrapy.Field()#经验

    education_background = scrapy.Field()#学历
    number_of_people = scrapy.Field()#人数
    bright_spots = scrapy.Field()#亮点
    position_information = scrapy.Field()#职位信息
    company_profile = scrapy.Field()#公司概况
