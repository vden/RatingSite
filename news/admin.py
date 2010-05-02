from django.contrib import admin
from news.models import *

class NewsAdmin(admin.ModelAdmin):
	list_display = ('date', 'title', 'published')
	search_fields = ['date', 'title',]
admin.site.register(News, NewsAdmin)
