from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import ugettext, ugettext_lazy as _
from django.template.context import RequestContext
from django.conf import settings
from django.template.defaultfilters import escapejs, force_escape
from django.views.decorators.http import require_POST

from cms.models import Page, Title, CMSPlugin, MASK_CHILDREN, MASK_DESCENDANTS,\
    MASK_PAGE
from cms.plugin_pool import plugin_pool
from cms.utils.admin import render_admin_menu_item
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from cms.utils import get_language_from_request


@require_POST
def change_status(request, page_id):
    """
    Switch the status of a page
    """
    page = get_object_or_404(Page, pk=page_id)
    if page.has_publish_permission(request):
        page.published = not page.published
        page.save(force_state=Page.MODERATOR_NEED_APPROVEMENT)    
        return render_admin_menu_item(request, page)
    else:
        return HttpResponseForbidden(ugettext("You do not have permission to publish this page"))
change_status = staff_member_required(change_status)

@require_POST
def change_innavigation(request, page_id):
    """
    Switch the in_navigation of a page
    """
    page = get_object_or_404(Page, pk=page_id)
    if page.has_change_permission(request):
        if page.in_navigation:
            page.in_navigation = False
            val = 0
        else:
            page.in_navigation = True
            val = 1
        page.save(force_state=Page.MODERATOR_NEED_APPROVEMENT)
        return render_admin_menu_item(request, page)
    return HttpResponseForbidden(ugettext("You do not have permission to change this page's in_navigation status"))
change_innavigation = staff_member_required(change_innavigation)

if 'reversion' in settings.INSTALLED_APPS:
    from reversion import revision    

def add_plugin(request):
    if 'history' in request.path or 'recover' in request.path:
        return HttpResponse(str("error"))
    if request.method == "POST":
        plugin_type = request.POST['plugin_type']
        page_id = request.POST.get('page_id', None)
        parent = None
        if page_id:
            page = get_object_or_404(Page, pk=page_id)
            placeholder = request.POST['placeholder'].lower()
            language = request.POST['language']
            position = CMSPlugin.objects.filter(page=page, language=language, placeholder=placeholder).count()
        else:
            parent_id = request.POST['parent_id']
            parent = get_object_or_404(CMSPlugin, pk=parent_id)
            page = parent.page
            placeholder = parent.placeholder
            language = parent.language
            position = None

        if not page.has_change_permission(request):
            return HttpResponseForbidden(ugettext("You do not have permission to change this page"))

        # Sanity check to make sure we're not getting bogus values from JavaScript:
        if not language or not language in [ l[0] for l in settings.LANGUAGES ]:
            return HttpResponseBadRequest(ugettext("Language must be set to a supported language!"))
        
        plugin = CMSPlugin(page=page, language=language, plugin_type=plugin_type, position=position, placeholder=placeholder) 

        if parent:
            plugin.parent = parent
        plugin.save()
        if 'reversion' in settings.INSTALLED_APPS:
            page.save()
            save_all_plugins(request, page)
            revision.user = request.user
            plugin_name = unicode(plugin_pool.get_plugin(plugin_type).name)
            revision.comment = _(u"%(plugin_name)s plugin added to %(placeholder)s") % {'plugin_name':plugin_name, 'placeholder':placeholder}
        return HttpResponse(str(plugin.pk))
    raise Http404

if 'reversion' in settings.INSTALLED_APPS:
    add_plugin = revision.create_on_success(add_plugin)

def edit_plugin(request, plugin_id, admin_site):
    plugin_id = int(plugin_id)
    if not 'history' in request.path and not 'recover' in request.path:
        cms_plugin = get_object_or_404(CMSPlugin, pk=plugin_id)
        instance, admin = cms_plugin.get_plugin_instance(admin_site)
        if not cms_plugin.page.has_change_permission(request):
            raise PermissionDenied 
    else:
        # history view with reversion
        from reversion.models import Version
        version_id = request.path.split("/edit-plugin/")[0].split("/")[-1]
        Version.objects.get(pk=version_id)
        version = get_object_or_404(Version, pk=version_id)
        revs = [related_version.object_version for related_version in version.revision.version_set.all()]
        # TODO: check permissions
        
        for rev in revs:
            obj = rev.object
            if obj.__class__ == CMSPlugin and obj.pk == plugin_id:
                cms_plugin = obj
                break
        inst, admin = cms_plugin.get_plugin_instance(admin_site)
        instance = None
        if cms_plugin.get_plugin_class().model == CMSPlugin:
            instance = cms_plugin
        else:
            for rev in revs:
                obj = rev.object
                if hasattr(obj, "cmsplugin_ptr_id") and int(obj.cmsplugin_ptr_id) == int(cms_plugin.pk):
                    instance = obj
                    break
        if not instance:
            raise Http404("This plugin is not saved in a revision")
    
    admin.cms_plugin_instance = cms_plugin
    admin.placeholder = cms_plugin.placeholder # TODO: what for reversion..? should it be inst ...?
    
    if request.method == "POST":
        # set the continue flag, otherwise will admin make redirect to list
        # view, which actually does'nt exists
        request.POST['_continue'] = True
    
    if 'reversion' in settings.INSTALLED_APPS and ('history' in request.path or 'recover' in request.path):
        # in case of looking to history just render the plugin content
        context = RequestContext(request)
        return render_to_response(admin.render_template, admin.render(context, instance, admin.placeholder))
    
    
    if not instance:
        # instance doesn't exist, call add view
        response = admin.add_view(request)
 
    else:
        # already saved before, call change view
        # we actually have the instance here, but since i won't override
        # change_view method, is better if it will be loaded again, so
        # just pass id to admin
        response = admin.change_view(request, str(plugin_id))
    
    if request.method == "POST" and admin.object_successfully_changed:
        # if reversion is installed, save version of the page plugins
        if 'reversion' in settings.INSTALLED_APPS:
            # perform this only if object was successfully changed
            cms_plugin.page.save()
            save_all_plugins(request, cms_plugin.page, [cms_plugin.pk])
            revision.user = request.user
            plugin_name = unicode(plugin_pool.get_plugin(cms_plugin.plugin_type).name)
            revision.comment = _(u"%(plugin_name)s plugin edited at position %(position)s in %(placeholder)s") % {'plugin_name':plugin_name, 'position':cms_plugin.position, 'placeholder': cms_plugin.placeholder}
            
        # read the saved object from admin - ugly but works
        saved_object = admin.saved_object
        
        context = {
            'CMS_MEDIA_URL': settings.CMS_MEDIA_URL, 
            'plugin': saved_object, 
            'is_popup': True, 
            'name': unicode(saved_object), 
            "type": saved_object.get_plugin_name(),
            'plugin_id': plugin_id,
            'icon': force_escape(escapejs(saved_object.get_instance_icon_src())),
            'alt': force_escape(escapejs(saved_object.get_instance_icon_alt())),
        }
        return render_to_response('admin/cms/page/plugin_forms_ok.html', context, RequestContext(request))
        
    return response

if 'reversion' in settings.INSTALLED_APPS:
    edit_plugin = revision.create_on_success(edit_plugin)

def move_plugin(request):
    if request.method == "POST" and not 'history' in request.path:
        pos = 0
        page = None
        for id in request.POST['ids'].split("_"):
            plugin = CMSPlugin.objects.get(pk=id)
            if not page:
                page = plugin.page
            
            if not page.has_change_permission(request):
                raise Http404

            if plugin.position != pos:
                plugin.position = pos
                plugin.save()
            pos += 1
        if page and 'reversion' in settings.INSTALLED_APPS:
            page.save()
            save_all_plugins(request, page)
            revision.user = request.user
            revision.comment = unicode(_(u"Plugins where moved")) 
        return HttpResponse("ok")
    else:
        raise Http404
    
if 'reversion' in settings.INSTALLED_APPS:
    move_plugin = revision.create_on_success(move_plugin)
  
def remove_plugin(request):
    if request.method == "POST" and not 'history' in request.path:
        plugin_id = request.POST['plugin_id']
        plugin = get_object_or_404(CMSPlugin, pk=plugin_id)
        page = plugin.page
        
        if not page.has_change_permission(request):
                raise Http404
        
        if settings.CMS_MODERATOR and page.is_under_moderation():
            plugin.delete()
        else:
            plugin.delete_with_public()
            
        plugin_name = unicode(plugin_pool.get_plugin(plugin.plugin_type).name)
        comment = _(u"%(plugin_name)s plugin at position %(position)s in %(placeholder)s was deleted.") % {'plugin_name':plugin_name, 'position':plugin.position, 'placeholder':plugin.placeholder}
        if 'reversion' in settings.INSTALLED_APPS:
            save_all_plugins(request, page)
            page.save()
            revision.user = request.user
            revision.comment = comment
        return HttpResponse("%s,%s" % (plugin_id, comment))
    raise Http404

if 'reversion' in settings.INSTALLED_APPS:
    remove_plugin = revision.create_on_success(remove_plugin)
    
def save_all_plugins(request, page, excludes=None):
    if not page.has_change_permission(request):
        raise Http404
    
    for plugin in CMSPlugin.objects.filter(page=page):
        if excludes:
            if plugin.pk in excludes:
                continue
        instance, admin = plugin.get_plugin_instance()
        if instance:
            instance.save()
        else:
            plugin.save()
        
def revert_plugins(request, version_id, obj):
    from reversion.models import Version
    version = get_object_or_404(Version, pk=version_id)
    revs = [related_version.object_version for related_version in version.revision.version_set.all()]
    cms_plugin_list = []
    plugin_list = []
    titles = []
    others = []
    page = obj
    lang = get_language_from_request(request)
    for rev in revs:
        obj = rev.object
        
        if obj.__class__ == CMSPlugin:
            cms_plugin_list.append(obj)
        elif hasattr(obj, 'cmsplugin_ptr_id'):
            plugin_list.append(obj)
        elif obj.__class__ == Page:
            pass
            #page = obj #Page.objects.get(pk=obj.pk)
        elif obj.__class__ == Title:
            if not obj.language == lang: 
                titles.append(obj) 
        else:
            others.append(rev)
    if not page.has_change_permission(request):
        raise Http404
    current_plugins = list(CMSPlugin.objects.filter(page=page))
    for plugin in cms_plugin_list:
        plugin.page = page
        plugin.save(no_signals=True)
    for plugin in cms_plugin_list:
        plugin.save()
        for p in plugin_list:
            if int(p.cmsplugin_ptr_id) == int(plugin.pk):
                plugin.set_base_attr(p)
                p.save()
        for old in current_plugins:
            if old.pk == plugin.pk:
                current_plugins.remove(old)
    for title in titles:
        title.page = page
        title.save()
    for other in others:
        other.object.save()
    for plugin in current_plugins:
        plugin.delete()

@require_POST
def change_moderation(request, page_id):
    """Called when user clicks on a moderation checkbox in tree vies, so if he
    wants to add/remove/change moderation required by him. Moderate is sum of
    mask values.
    """
    page = get_object_or_404(Page, id=page_id)
    moderate = request.POST.get('moderate', None)
    if moderate is not None and page.has_moderate_permission(request):
        try:
            moderate = int(moderate)
        except:
            moderate = 0
        
        if moderate == 0:
            # kill record with moderation which equals zero
            try:
                page.pagemoderator_set.get(user=request.user).delete()
            except ObjectDoesNotExist:
                pass
            return render_admin_menu_item(request, page)
        elif moderate <= MASK_PAGE + MASK_CHILDREN + MASK_DESCENDANTS:
            page_moderator, created = page.pagemoderator_set.get_or_create(user=request.user)
            # split value to attributes
            page_moderator.set_decimal(moderate)
            page_moderator.save()
            return render_admin_menu_item(request, page)
    raise Http404
