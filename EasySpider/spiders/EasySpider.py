import urlparse
import scrapy
from items import EasyspiderItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from helpers import *
import MySQLdb

class EasySpider(scrapy.Spider):
	name = "qdmm"
	allowed_domains = ["qdmm.com"]
	curr_page = get_page_from_file()
	start_urls = get_start_url()

	#rules = (Rule(LinkExtractor(restrict_xpaths = '//a[@class="f_a"]'), callback = 'parse_item', follow = True,),)


	def parse(self, response):

		#while len(self.crawler.engine.slot.scheduler) > 0 or len(self.crawler.engine.slot.inprogress) > 1:
			#pass

		links = response.xpath('//a/@href').extract()
		for link in links:
			if is_book_page(link):
				update_time = get_update_time(link, response)
				if needs_update(update_time):
					page = get_page_from_url(response.url)
					yield self.newItem(link, page)

		next_pages = response.xpath('//a[@class="f_a"]/@href').extract()
		for url in next_pages:
			page_num = get_page_from_url(url)
			if page_num > self.curr_page:
				self.curr_page = page_num
				yield scrapy.Request('http://all.qdmm.com'+url, callback = self.parse, priority = -page_num)
				break



	def newItem(self, link, page):

		item = EasyspiderItem()
		item['link'] = link
		item['page'] = page
		item['key'] = link.replace('http://www.qdmm.com/MMWeb/', '').replace('.aspx', '')

		request = scrapy.Request(link, callback = self.parse_book_page, priority = -page)
		request.meta['item'] = item

		return request


	def parse_book_page(self, response):
		item = response.meta['item']
		
		sel = response.xpath('//div[@class="box_cont"]')
		item['title'] = sel.xpath('//strong[@itemprop="name"]/text()').extract_first(default = 'not found').strip()
		item['author'] = sel.xpath('//span[@itemprop="author"]/a/span/text()').extract_first(default = 'not found').strip()
		item['cover_url'] = sel.xpath('//div[@class="pic_box"]/a/img/@src').extract_first(default = 'not found').strip()
		item['image_urls'] = [item['cover_url']]
		item['intro'] = get_intro(sel.xpath('//div[@class="txt"]/span[@itemprop="description"]/text()').extract())
		#item['intro'] = sel.xpath('//span[@itemprop="description"]/text()').extract_first(default = 'not found').strip()
		item['catalog'] = sel.xpath('//span[@itemprop="trialStatus"]/text()').extract_first(default = 'not found').strip()
		item['total_hit'] = sel.xpath('//span[@itemprop="totalClick"]/text()').extract_first(default = 'not found').strip()
		item['month_hit'] = sel.xpath('//span[@itemprop="monthlyClick"]/text()').extract_first(default = 'not found').strip()
		item['week_hit'] = sel.xpath('//span[@itemprop="weeklyClick"]/text()').extract_first(default = 'not found').strip()
		item['genre'] = sel.xpath('//span[@itemprop="genre"]/text()').extract_first(default = 'not found').strip()
		item['total_recmd'] = sel.xpath('//span[@itemprop="totalRecommend"]/text()').extract_first(default = 'not found').strip()
		item['month_recmd'] = sel.xpath('//span[@itemprop="monthlyRecommend"]/text()').extract_first(default = 'not found').strip()
		item['week_recmd'] = sel.xpath('//span[@itemprop="weeklyRecommend"]/text()').extract_first(default = 'not found').strip()
		item['progress'] = sel.xpath('//span[@itemprop="updataStatus"]/text()').extract_first(default = 'not found').strip()
		item['word_count'] = sel.xpath('//span[@itemprop="wordCount"]/text()').extract_first(default = 'not found').strip()
		time = sel.xpath('//div[@class="book_info"]/div/div[@class="right"]/text()').extract_first(default = 'not found').strip()
		try:
			item['update_time'] = time[time.index("2"):] + ":00"
			assert (len(item['update_time']) > 15) 
		except:
			item['update_time'] = 'not found'

		link = sel.xpath('//div[@class="opt"]/ul/li/a/@href').extract()[0]
		link = 'http://www.qdmm.com'+link

		request = scrapy.Request(link, callback = self.parse_chap_page, priority = -item['page'])
		request.meta['item'] = item

		return request


	def parse_chap_page(self, response):
		item = response.meta['item']

		norm_chap_name = response.xpath('//span[@itemprop="headline"]/text()').extract()
		norm_chap_url = response.xpath('//li[@itemprop="chapter"]/a/@href').extract()
		vip_chap_name = response.xpath('//li[@style="width:33%;"]/a[@rel="nofollow"]/text()').extract()
		vip_chap_url = response.xpath('//li[@style="width:33%;"]/a[@rel="nofollow"]/@href').extract()
		chapter = combine(norm_chap_name, norm_chap_url, 'http://www.qdmm.com')
		chapter.extend(combine(vip_chap_name, vip_chap_url))
		item['chapter_info'] = chapter

		return item




