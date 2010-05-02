from news.models import News

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.template import RequestContext


def index(request, page):
    res = News.objects.all().order_by('-date')
    return render_to_response("news/index.html", {'res': res}, context_instance=RequestContext(request))

@login_required
def show_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)

    return render_to_response("news/news.html", {'obj': news}, context_instance=RequestContext(request))
