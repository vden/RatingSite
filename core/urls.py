from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'core.views.index', name="core_index"),

)
