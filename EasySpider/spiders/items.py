# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class EasyspiderItem(Item):
    # define the fields for your item here like:
    title = Field() # 小说名
    author = Field() # 作者
    link = Field() # 链接
    key = Field()
    page = Field()
    cover_url = Field() # 封面
    image_urls = Field()
    images = Field()

    intro = Field() # 内容简介

    catalog = Field() # 小说性质
    genre = Field() # 小说类别
    progress = Field() # 写作进程

    total_hit = Field() # 总点击
    total_recmd = Field() # 总推荐
    month_hit = Field() # 月点击
    month_recmd = Field() # 月推荐
    week_hit = Field() # 周点击
    week_recmd = Field() # 周推荐

    word_count = Field() # 完成字数

    chapter_info = Field() # 章节信息

    update_time = Field()
    added_time = Field()

    pass
