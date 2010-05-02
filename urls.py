from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^rating/', include('rating.urls')),
	(r'^news/', include('news.urls')),
	(r'^graphic/', include('graphic.urls')),

	(r'^admin/', include(admin.site.urls)),
	(r'^openid/', include('django_openid_auth.urls')),
	(r'^logout/$', 'django.contrib.auth.views.logout'),

	(r'^', include('core.urls')),
)
