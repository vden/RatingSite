from django.template import loader, TemplateDoesNotExist
from cms.utils import get_template_from_request
from django.template.context import RequestContext
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site
import re

def get_placeholders(request, template_name):
    """
    Return a list of PlaceholderNode found in the given template
    """
    try:
        temp = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return []
    user = request.user
    request.user = AnonymousUser()
    context = RequestContext(request)#details(request, no404=True, only_context=True)
    template = get_template_from_request(request)
    request.current_page = "dummy"
    
    context.update({'template':template,
                    'request':request,
                    'display_placeholder_names_only': True,
                    'current_page': "dummy",
                    })
    output = temp.render(context)
    request.user = user
    return re.findall("<!-- PlaceholderNode: (.+?) -->", output)


SITE_VAR = "site__exact"

def current_site(request):
    if SITE_VAR in request.REQUEST:
        return Site.objects.get(pk=request.REQUEST[SITE_VAR])
    else:
        site_pk = request.session.get('cms_admin_site', None)
        if site_pk:
            return Site.objects.get(pk=site_pk)
        else:
            return Site.objects.get_current()
        