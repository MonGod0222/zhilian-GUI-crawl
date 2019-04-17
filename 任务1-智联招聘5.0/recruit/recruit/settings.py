# -*- coding: utf-8 -*-

# Scrapy settings for recruit project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'recruit'

SPIDER_MODULES = ['recruit.spiders']
NEWSPIDER_MODULE = 'recruit.spiders'

MAX_PAGE = 1

MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'zhilian'

MYSQL_PORT = 3306

MONGO_URI = 'localhost'
MONGO_DB = 'zhilian'
MONGO_COLLECTION = ''

MYSQL_SWITCH = None
MONGO_SWITCH = None

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'recruit (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False



DOWNLOADER_MIDDLEWARES = {
    'recruit.middlewares.IndexDownloaderMiddleware': 543,
    'recruit.middlewares.ContentDownloaderMiddleware': 544
}


ITEM_PIPELINES = {
    'recruit.pipelines.MysqlPipeline':300,
    'recruit.pipelines.MongoPipeline':301
}
#默认300

