# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import shutil
import requests
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonLinesItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
import logging
import json
from datetime import datetime
import sys
import django

#sys.path.append('/Users/mac/Desktop/EasySpider/qdmmDjango/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'qdmmDjango.settings'
django.setup()

from qdmm.models import BookInfo


ITEM_PER_DIR = 1000

def get_data_dir(key):
	return "./EasySpider/data/" + str(int(int(key)/ITEM_PER_DIR)*ITEM_PER_DIR)

def get_image_dir(key):
	return "./EasySpider/cover/" + str(int(int(key)/ITEM_PER_DIR)*ITEM_PER_DIR)


class FilterDupPipeline(object):

	def __init__(self):
		self.visited = set()

	def process_item(self, item, spider):
		if item['key'] in self.visited:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.visited.add(item['key'])
			return item

class JsonlinesWriterPipeline(object):


	def process_item(self, item, spider):
		directory = get_data_dir(item['key'])
		if not os.path.exists(directory):
			os.makedirs(directory)

		write_file = directory + "/" + item['key'] + ".jsonlines"
		f = open(write_file, "w")
		exporter = JsonLinesItemExporter(f)
		exporter.start_exporting()
		exporter.export_item(item)
		exporter.finish_exporting()
		f.close()


		return item


class ImageDownloadPipeline(object):

	def process_item(self, item, spider):
		directory = get_image_dir(item['key'])
		if not os.path.exists(directory):
			os.makedirs(directory)

		write_file = directory + "/" + item['key'] + ".jpg"
		response = requests.get(item['cover_url'], stream = True)
		f = open(write_file, "wb")
		shutil.copyfileobj(response.raw, f)
		del response
		
		return item

class SQLStorePipeline(object):

	def __init__(self, dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls, settings):
		dbargs = dict(
			host = settings['MYSQL_HOST'],
			db = settings['MYSQL_DBNAME'],
			user = settings['MYSQL_USER'],
			passwd = settings['MYSQL_PASSWORD'],
			charset = settings['MYSQL_CHARSET'],
			cursorclass = MySQLdb.cursors.DictCursor,
			use_unicode = True,
			)

		dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
		return cls(dbpool)

	def process_item(self, item, spider):
		db = self.dbpool.runInteraction(self._store_item, item, spider)
		db.addErrback(self._handle_error, item, spider)

		return item


	def _store_item(self, conn, item, spider):
		
		conn.execute("select 1 from qdmminfo where `key` = %s", (item['key'], ))
		exists = conn.fetchone()

		if exists:
			conn.execute("""
					update qdmminfo set `cover_url` = %s, `intro` = %s, `progress` = %s, `total_hit` = %s, `total_recmd` = %s, `month_hit` = %s, `month_recmd` = %s, `week_hit` = %s, `week_recmd` = %s, `word_count` = %s, `chapter_info` = %s, `update_time` = %s, `added_time` = %s where `key` = %s
				""", (item['cover_url'], json.dumps(item['intro'], ensure_ascii = False),
					item['progress'], item['total_hit'], item['total_recmd'], item['month_hit'],
					item['month_recmd'], item['week_hit'], item['week_recmd'], item['word_count'],
					json.dumps(item['chapter_info'], ensure_ascii = False), item['update_time'], datetime.now(), item['key']))
		else:
			conn.execute("""
					insert into qdmminfo(`title`, `author`, `link`, `key`, `cover_url`, `intro`, `catalog`, `genre`, `progress`, `total_hit`, `total_recmd`, `month_hit`, `month_recmd`, `week_hit`, `week_recmd`, `word_count`, `chapter_info`, `update_time`, `added_time`, `created_time`) 
					values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
				""", (item['title'], item['author'], item['link'], item['key'],
					item['cover_url'], json.dumps(item['intro'], ensure_ascii = False), item['catalog'], 
					item['genre'], item['progress'], item['total_hit'], item['total_recmd'], item['month_hit'],
					item['month_recmd'], item['week_hit'], item['week_recmd'], item['word_count'],
					json.dumps(item['chapter_info'], ensure_ascii = False), item['update_time'], datetime.now(), datetime.now()))

	def _handle_error(self, failure, item, spider):
		logging.error(failure)

class DjangoImageStorePipeline(ImagesPipeline):
	def file_path(self, request, response = None, info = None):
		return request.url.split("/")[-1]

	def get_media_request(self, item, info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):
		try:
			if results[0][0] == False:
				item['cover_url'] = 'http://image.cmfu.com/Books/0.jpg'
		except:
			item['cover_url'] = 'http://image.cmfu.com/Books/0.jpg'
		return item

class DjangoStorePipeline(object):

	def process_item(self, item, spider):
		
		try:
			book_info = BookInfo.objects.get(key = item['key'])
			book_info.cover_url = item['cover_url']
			book_info.cover = 'media/'+item['cover_url'].split("/")[-1]
			book_info.intro = json.dumps(item['intro'], ensure_ascii = False)
			book_info.progress = item['progress']
			book_info.total_hit = item['total_hit']
			book_info.total_recmd = item['total_recmd']
			book_info.month_hit = item['month_hit']
			book_info.month_recmd = item['month_recmd']
			book_info.week_hit = item['week_hit']
			book_info.week_recmd = item['week_recmd']
			book_info.word_count = item['word_count']
			book_info.chapter_info = json.dumps(item['chapter_info'], ensure_ascii = False)
			book_info.update_time = item['update_time']
			book_info.added_time = datetime.now()
			book_info.save()
		except BookInfo.DoesNotExist:
			book_info = BookInfo(title = item['title'], author = item['author'],
				link = item['link'], key = item['key'], cover_url = item['cover_url'],
				cover = 'media/'+item['cover_url'].split("/")[-1],
				intro = json.dumps(item['intro'], ensure_ascii = False),
				catalog = item['catalog'], genre = item['genre'], progress = item['progress'],
				total_hit = item['total_hit'], total_recmd = item['total_recmd'], 
				month_hit = item['month_hit'], month_recmd = item['month_recmd'],
				week_hit = item['week_hit'], week_recmd = item['week_recmd'],
				word_count = item['word_count'], 
				chapter_info = json.dumps(item['chapter_info'], ensure_ascii = False),
				created_time = datetime.now(), update_time = item['update_time'],
				added_time = datetime.now())
			book_info.save()
		
		"""
		directory = './qdmmDjango/qdmmCollect/static'
		if not os.path.exists(directory):
			os.makedirs(directory)

		write_file = directory + "/" + item['key'] + ".jpg"
		response = requests.get(item['cover_url'], stream = True)
		if response.status_code == 404:
			response = requests.get('http://image.cmfu.com/Books/0.jpg', stream = True)
		f = open(write_file, "wb")
		shutil.copyfileobj(response.raw, f)
		del response
		"""

		return item




