from cms.utils import get_page_from_request
from cms.models.pagemodel import Page

class LazyPage(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_current_page_cache'):
            request._current_page_cache = get_page_from_request(request) or Page.objects.filter(soft_root=True)[0]
        return request._current_page_cache
    
class CurrentPageMiddleware(object):
    def process_request(self, request):
        request.__class__.current_page = LazyPage()
        return None
