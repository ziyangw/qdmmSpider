# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EasyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field() # 小说名
    author = scrapy.Field() # 作者
    link = scrapy.Field() # 链接
    key = scrapy.Field()
    page = scrapy.Field()
    cover_url = scrapy.Field() # 封面
    image_urls = scrapy.Field()
    images = scrapy.Field()

    intro = scrapy.Field() # 内容简介

    catalog = scrapy.Field() # 小说性质
    genre = scrapy.Field() # 小说类别
    progress = scrapy.Field() # 写作进程

    total_hit = scrapy.Field() # 总点击
    total_recmd = scrapy.Field() # 总推荐
    month_hit = scrapy.Field() # 月点击
    month_recmd = scrapy.Field() # 月推荐
    week_hit = scrapy.Field() # 周点击
    week_recmd = scrapy.Field() # 周推荐

    word_count = scrapy.Field() # 完成字数

    chapter_info = scrapy.Field() # 章节信息

    update_time = scrapy.Field()
    added_time = scrapy.Field()


    pass
