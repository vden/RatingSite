from news.models import News
from feeds.models import IndexedArticle

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from django.template import RequestContext

def index(request):
	return  render_to_response("core/index.html", {'news': News.last(), 'feed': IndexedArticle.objects.order_by('-pubdate')[:10]}, context_instance=RequestContext(request))

def aim(request, path):
	return  render_to_response("core/aim.html", {}, context_instance=RequestContext(request))

def bookmarks_by_tag(request, tag):

    tag = urllib.unquote(unicode(tag))
    tag = get_object_or_404(Tag, name = tag)

    bookmark_instances = TaggedItem.objects.get_by_model(BookmarkInstance, tag)

    return render_to_response("core/tag.html", { "bookmark_instances": bookmark_instances, }, context_instance=RequestContext(request))
