from news.models import News
from feeds.models import IndexedArticle

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from django.template import RequestContext

def index(request):
	return  render_to_response("core/index.html", {'news': News.last(), 'feed': IndexedArticle.objects.order_by('-pubdate')[:10]}, context_instance=RequestContext(request))
