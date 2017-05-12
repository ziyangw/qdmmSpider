
from scrapy import signals
from scrapy.statscollectors import StatsCollector
from scrapy.exceptions import NotConfigured
from time import strftime
import os

class RecordUpdateStatus(object):

    @classmethod
    def from_crawler(cls, crawler):

        ext = cls()

        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        ext.crawler = crawler

        return ext


    def spider_closed(self, spider, reason):

        error = self.crawler.stats.get_value('log_count/ERROR')

        if reason == "finished" and error == None:
            self.write_success_update()
        else:
            if reason == "finished":
                reason = "error"
            self.write_failure_update(reason)


    def item_scraped(self, item, response, spider):

        url = 'http://all.qdmm.com/MMWeb/BookStore.aspx?ChannelId=41&SubCategoryId=-1&Tag=all&Size=-1&Action=-1&OrderId=6&P=all&PageIndex=%d&update=-1&Vip=-1' % item['page']

        path = './EasySpider/status.txt'

        if not os.path.isfile(path):
            f = open(path, "w")
            f.write("Crawling: %s" % url)
            f.close()
            return

        f = open(path, "r")
        lines = f.readlines()
        f.close()

        f = open(path, "w")
        if len(lines) < 2:
            f.write("Crawling: %s" % url)
        else:
            f.write("Crawling: %s\n%s" % (url, lines[1]))

        f.close()

    	return


    def write_success_update(self):

        path = './EasySpider/status.txt'
        f = open(path, "w")

        time = strftime("%y-%m-%d %H:%M")
        cont = 'finished: %s\nlast_finished: %s' % (time, time)
        f.write(cont)
        f.close()

        return

    def write_failure_update(self, reason):

        path = './EasySpider/status.txt'

        if not os.path.isfile(path):
            f = open(path, "w")
            f.write(reason)
            f.close()
            return

        f = open(path, "r")
        lines = f.readlines()
        f.close()

        f = open(path, "w")
        if lines[0].startswith("Crawling: "):
            if len(lines) >= 2:
                f.write("%s%s" % (lines[0].replace("Crawling", reason), lines[1]))
            else:
                f.write("%s" % lines[0].replace("Crawling", reason))
        else:
            if len(lines) >= 2:
                f.write("%s\n%s" % (reason, lines[1]))
            else:
                f.write("%s" % reason)

        return