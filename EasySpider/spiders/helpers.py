import os
import re


def get_page_from_file():

	path = './EasySpider/status.txt'
	if not os.path.isfile(path):
		return 1

	f = open(path)
	lines = f.readlines()
	f.close()

	if lines[0].startswith("finished"):
		return 1

	try:
		return int(re.findall('\d+', lines[0])[5])
	except:
		return 1



def get_page_from_url(url):
	if not (url.startswith('/MMWeb/BookStore.aspx?') or url.startswith('http://all.qdmm.com/MMWeb/BookStore.aspx?')):
		return 1
	else:
		return int(re.findall('\d+', url)[5])


def get_start_url():
	default_url = ['http://all.qdmm.com/MMWeb/BookStore.aspx?ChannelId=41&SubCategoryId=-1&Tag=all&Size=-1&Action=-1&OrderId=6&P=all&PageIndex=1&update=-1&Vip=-1']

	path = './EasySpider/status.txt'
	if not os.path.isfile(path):
		return default_url

	f = open(path)
	lines = f.readlines()


	if lines[0].startswith("finished"):
		f.close()
		return default_url
	else:
		url = ['http://all.qdmm.com/MMWeb/BookStore.aspx?ChannelId=41&SubCategoryId=-1&Tag=all&Size=-1&Action=-1&OrderId=6&P=all&PageIndex=%d&update=-1&Vip=-1' % get_page_from_file()]
		f.close()
		return url

def is_book_page(link):
	if (link.startswith('http://www.qdmm.com/MMWeb/') 
		    and link.endswith('.aspx')):
		link = link.replace('http://www.qdmm.com/MMWeb/', '').replace('.aspx', '')
		return link.isdigit()
	return False



def get_update_time(link, response):
	return response.xpath('//a[@href="%s"]/../../../div[@class="swe"]/text()' % link).extract_first(default = 'not found').strip()



def needs_update(time):
	# time in form of yr-mth-day hr:min
	# example: 16-08-11 14:01
	if time == "not found":
		return False

	path = './EasySpider/status.txt'
	if not os.path.isfile(path):
		return True

	f = open(path)
	lines = f.readlines()
	if len(lines) < 2:
		return True

	for line in lines:
		if line.startswith("finished: "):
			line = line.replace("finished: ", "")
			last_time = line
			break
		if line.startswith("last_finished: "):
			line = line.replace("last_finished: ", "")
			last_time = line
			break

	f.close()

	update_yr = int(time[0:2])
	update_mth = int(time[3:5])
	update_day = int(time[6:8])
	update_hr = int(time[9:11])
	update_min = int(time[12:])

	last_yr = int(last_time[0:2])
	last_mth = int(last_time[3:5])
	last_day = int(last_time[6:8])
	last_hr = int(last_time[9:11])
	last_min = int(last_time[12:])

	if update_yr < last_yr: return False
	if update_yr > last_yr: return True

	if update_mth < last_mth: return False
	if update_mth > last_mth: return True

	if update_day < last_day: return False
	if update_day > last_day: return True

	if update_hr < last_hr: return False
	if update_hr > last_hr: return True

	if update_min < last_min: return False
	if update_min > last_min: return True

	return True


def get_intro(L):
	if len(L) < 2: return L

	first_line = L[0]
	result = [first_line]

	for line in L[1:]:
		if line == first_line:
			break
		else:
			result.append(line)

	return result

def combine(l1, l2, header = ""):
	result = []
	for i in range(len(l1)):
		result.append((l1[i], header+l2[i]))

	return result

