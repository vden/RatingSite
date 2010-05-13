from django.contrib import admin
from feeds.models import *

class IndexedBlogAdmin(admin.ModelAdmin):
	list_display = ('url', 'owner', 'published')
	search_fields = ['url', 'owner_name']
	list_filter = [ 'published']
admin.site.register(IndexedBlog, IndexedBlogAdmin)


class IndexedArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'pubdate', 'blog')
	search_fields = ['pubdate', 'title',]
admin.site.register(IndexedArticle, IndexedArticleAdmin)

class StatCategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)
admin.site.register(StatCategory, StatCategoryAdmin)

class StatAtomAdmin(admin.ModelAdmin):
	list_display = ('category', "value")
	search_fields = ['blog',]
admin.site.register(StatAtom, StatAtomAdmin)
