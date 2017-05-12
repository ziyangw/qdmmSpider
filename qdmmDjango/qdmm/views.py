from django.shortcuts import render
from django.http import HttpResponse
from .models import BookInfo
from django.template import loader
from django.db.models import Q
import math
import json
from django.views.decorators.cache import cache_page

# Create your views here.
genres = BookInfo.objects.values_list('genre').distinct()
if len(genres) >= 10:
	dropdown_genres = genres[10:]
	genres = genres[:10]
else:
	dropdown_genres=[]
objects = BookInfo.objects.order_by('-update_time')

@cache_page(60 * 15)
def index(request):
	#book_list = BookInfo.objects.order_by('-update_time')[:12]
	#genres = BookInfo.objects.values_list('genre').distinct()
	book_list = objects[:12]
	template = loader.get_template('qdmm/index.html')
	pages = range(1, 11)
	context = {
		'book_list': book_list,
		'pages': pages,
		'curr_page': 1,
		'prev_page': 1,
		'next_page': 2,
		'genres': genres,
		'dropdown_genres':dropdown_genres,
	}
	return HttpResponse(template.render(context, request))

@cache_page(60 * 15)
def index_page(request, page_num):
	curr_page = int(page_num)
	prev_page = curr_page - 1
	next_page = curr_page + 1
	start, end = 12*(curr_page-1), 12*curr_page
	#book_list = BookInfo.objects.order_by('-update_time')[start:end]
	#genres = BookInfo.objects.values_list('genre').distinct()
	book_list = objects[start:end]
	template = loader.get_template('qdmm/index.html')
	if (curr_page < 6):
		pages = range(1, 11)
	elif (curr_page > 995):
		if (curr_page > 1000):
			pages = []
		else:
			pages = range(991, 1001)
	else:
		pages = range(curr_page-4, curr_page+6)
	context = {
		'book_list': book_list,
		'pages': pages,
		'curr_page': curr_page,
		'prev_page': prev_page,
		'next_page': next_page,
		'genres': genres,
		'dropdown_genres':dropdown_genres,
	}
	return HttpResponse(template.render(context, request))


def book(request, key):
	item = BookInfo.objects.get(key = key)
	chap_info = json.loads(item.chapter_info, encoding="utf-8")
	genre_list = objects.filter(genre = item.genre)
	recmd_list = genre_list.order_by('-total_recmd')
	try:
		recmd_list = recmd_list[:10]
	except: pass
	hit_list = genre_list.order_by('-total_hit')
	try:
		hit_list = hit_list[:10]
	except: pass
	template = loader.get_template('qdmm/book.html')
	context = {
		'book': item,
		'chap_info': chap_info,
		'genres': genres,
		'dropdown_genres':dropdown_genres,
		'recmd_list': recmd_list,
		'hit_list': hit_list,
	}
	return HttpResponse(template.render(context, request))

@cache_page(60 * 15)
def genre(request, page, key):
	curr_page = int(page)
	prev_page = curr_page - 1
	next_page = curr_page + 1
	start, end = 12*(curr_page-1), 12*curr_page
	#book_list = BookInfo.objects.filter(genre = key).order_by('-update_time')[start:end]
	filtered = objects.filter(genre = key)
	max_page = min(int(math.ceil(math.ceil(len(filtered)/12)+0.5)), 1000)
	book_list = filtered[start:end]
	#genres = BookInfo.objects.values_list('genre').distinct()
	template = loader.get_template('qdmm/genre.html')
	if (curr_page + 6 <= max_page):
		if (curr_page < 6):
			pages = range(1, min(11, max_page))
		elif (curr_page > 995):
			if (curr_page > 1000):
				pages = []
			else:
				pages = range(991, 1001)
		else:
			pages = range(curr_page-4, curr_page+6)
	else:
		pages = range(max(max_page-9, 1), max_page+1)
	if next_page > max_page:
		next_page = curr_page
	context = {
		'book_list': book_list,
		'pages': pages,
		'curr_page': curr_page,
		'prev_page': prev_page,
		'next_page': next_page,
		'genres': genres,
		'dropdown_genres':dropdown_genres,
		'curr_genre': key,
		'max_page': max_page,
	}
	return HttpResponse(template.render(context, request))

def search(request, page, key):
	curr_page = int(page)
	prev_page = curr_page - 1
	next_page = curr_page + 1
	start, end = 12*(curr_page-1), 12*curr_page
	#book_list = BookInfo.objects.filter(genre = key).order_by('-update_time')[start:end]
	filtered = objects.filter(Q(title__contains=key) | Q(author__contains=key) | Q(intro__contains=key) | Q(genre__contains=key))
	max_page = min(int(math.ceil(math.ceil(len(filtered)/12)+0.5)), 1000)
	book_list = filtered[start:end]
	#genres = BookInfo.objects.values_list('genre').distinct()
	template = loader.get_template('qdmm/search.html')
	if (curr_page + 6 <= max_page):
		if (curr_page < 6):
			pages = range(1, min(11, max_page))
		elif (curr_page > 995):
			if (curr_page > 1000):
				pages = []
			else:
				pages = range(991, 1001)
		else:
			pages = range(curr_page-4, curr_page+6)
	else:
		pages = range(max(max_page-9, 1), max_page+1)
	if next_page > max_page:
		next_page = curr_page
	context = {
		'book_list': book_list,
		'pages': pages,
		'curr_page': curr_page,
		'prev_page': prev_page,
		'next_page': next_page,
		'genres': genres,
		'dropdown_genres':dropdown_genres,
		'curr_search': key,
		'max_page': max_page,
	}
	return HttpResponse(template.render(context, request))

@cache_page(60 * 15)
def recommand(request):
	total_recmd_list = BookInfo.objects.order_by('-total_recmd')[:10]
	month_recmd_list = BookInfo.objects.order_by('-month_recmd')[:10]
	week_recmd_list = BookInfo.objects.order_by('-week_recmd')[:10]
	total_hit_list = BookInfo.objects.order_by('-total_hit')[:10]
	month_hit_list = BookInfo.objects.order_by('-month_hit')[:10]
	week_hit_list = BookInfo.objects.order_by('-week_hit')[:10]
	template = loader.get_template('qdmm/recommand.html')
	context={
		'total_recmd_list': total_recmd_list,
		'month_recmd_list': month_recmd_list,
		'week_recmd_list': week_recmd_list,
		'total_hit_list': total_hit_list,
		'month_hit_list': month_hit_list,
		'week_hit_list': week_hit_list,
		'genres': genres,
		'dropdown_genres': dropdown_genres,
	}
	return HttpResponse(template.render(context, request))

def about(request):
	template = loader.get_template('qdmm/about.html')
	context={}
	return HttpResponse(template.render(context, request))

