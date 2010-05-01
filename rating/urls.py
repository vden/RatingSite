from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'rating.views.index', name="rating_index"),

)
