from django.contrib import admin
from rating.models import *

class TakeRequestAdmin(admin.ModelAdmin):
	list_display = ('blog', 'author', 'date')
	search_fields = ['blog', 'date']
admin.site.register(TakeRequest, TakeRequestAdmin)
