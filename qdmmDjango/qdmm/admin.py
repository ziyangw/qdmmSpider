from django.contrib import admin
from .models import BookInfo

# Register your models here.
class BookInfoAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'genre', 'catalog', 'update_time', 'book_cover')
	list_filter = ['update_time', 'catalog', 'genre']
	search_fields = ('title', 'author', 'genre')
	date_hierarchy = 'update_time'
	ordering = ('-update_time', 'added_time')
	fieldsets = [
		('Basic Information', {'fields': ['title', 'author', 'link', 'catalog', 'genre', 'progress', 'intro']}),
		('Cover', {'fields': ['cover']}),
		('Updates', {'fields': ['update_time', 'added_time', 'created_time']}),
		('Stats', {'fields': ['total_hit', 'month_hit', 'week_hit', 'total_recmd', 'month_recmd', 'week_recmd', 'word_count'], 'classes': ['collapse']}),
		('Chapters', {'fields': ['chapter_info'], 'classes': ['collapse']})
	]



admin.site.register(BookInfo, BookInfoAdmin)