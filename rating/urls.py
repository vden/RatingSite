from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'^$', 'rating.views.index', name="rating_index"),
	url(r'^card/(?P<blog_id>\d+)/$', 'rating.views.card', name="rating_card"),
	url(r'^card/(?P<blog_id>\d+)/take/$', 'rating.views.take', name="take_card"),
	url(r'^articles/(?P<blog_id>\d+)/(?P<category_id>.*)/$', 'rating.views.articles', name="list-articles"),
	url(r'^card/(?P<blog_id>\d+)/save/$', 'rating.views.save_info', name="save-info"),
)
