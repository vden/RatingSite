from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'core.views.index', name="core_index"),
	url(r'^tag/(?P<tag>[^/]+)/$', bookmarks_by_tag, name = "tag"),

)
