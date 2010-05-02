from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'graphic.views.index', name="graphic_index"),

)
