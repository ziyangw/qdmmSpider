# -*- coding: UTF-8 -*- 
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class BookInfo(models.Model):

	title = models.CharField(max_length = 200) # 小说名
	author = models.CharField(max_length = 100) # 作者
	link = models.CharField(max_length = 300) # 链接
	key = models.BigIntegerField(db_index = True)
	cover_url = models.CharField(max_length = 300) # 封面
	cover = models.ImageField(upload_to = 'media')

	intro = models.TextField() # 内容简介

	catalog = models.CharField(max_length = 100) # 小说性质
	genre = models.CharField(max_length = 100) # 小说类别
	progress = models.CharField(max_length = 100) # 写作进程

	total_hit = models.CharField(max_length = 50) # 总点击
	total_recmd = models.CharField(max_length = 20) # 总推荐
	month_hit = models.CharField(max_length = 20) # 月点击
	month_recmd = models.CharField(max_length = 20) # 月推荐
	week_hit = models.CharField(max_length = 20) # 周点击
	week_recmd = models.CharField(max_length = 20) # 周推荐

	word_count = models.CharField(max_length = 50) # 完成字数

	chapter_info = models.TextField() # 章节信息

	created_time = models.DateTimeField()
	update_time = models.DateTimeField()
	added_time = models.DateTimeField()

	def book_cover(self):
		return '<img src="%s"/>' % self.cover.url
	book_cover.allow_tags = True

	def __unicode__(self):
		return self.title
