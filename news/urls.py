from django.conf.urls.defaults import *

urlpatterns = patterns('news.views',
               url(r'^$', 'index', {'page': None}, name="news_index"),
               (r'^(?P<news_id>\d+)/', 'show_news'),
               (r'^', include('cms.urls')),
)
