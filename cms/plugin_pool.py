from cms.exceptions import PluginAllreadyRegistered
from django.conf import settings
from cms.plugin_base import CMSPluginBase
from cms.utils.helpers import reversion_register

class PluginPool(object):
    def __init__(self):
        self.plugins = {}
        self.discovered = False
        
    def discover_plugins(self):
        if self.discovered:
            return
        for app in settings.INSTALLED_APPS:
            __import__(app, {}, {}, ['cms_plugins']) 
        self.discovered = True
    
    def register_plugin(self, plugin):
        #from cms.plugins import CMSPluginBase
        assert issubclass(plugin, CMSPluginBase)
        if plugin.__name__ in self.plugins.keys():
            raise PluginAllreadyRegistered, "[%s] a plugin with this name is already registered" % plugin.__name__
        plugin.value = plugin.__name__
        self.plugins[plugin.__name__] = plugin 
        
        if 'reversion' in settings.INSTALLED_APPS:   
            try:
                from reversion.registration import RegistrationError
            except ImportError:
                from reversion.revisions import RegistrationError
            try:
                reversion_register(plugin.model, follow=["cmsplugin_ptr"])
            except RegistrationError:
                pass
    
    def get_all_plugins(self, placeholder=None):
        self.discover_plugins()
        plugins = self.plugins.values()[:]
        plugins.sort(key=lambda obj: unicode(obj.name))
        if placeholder:
            final_plugins = []
            for plugin in plugins:
                found = True
                if settings.CMS_PLACEHOLDER_CONF:
                    if placeholder in settings.CMS_PLACEHOLDER_CONF:
                        if "plugins" in settings.CMS_PLACEHOLDER_CONF[placeholder] \
                        and not plugin.__name__ in settings.CMS_PLACEHOLDER_CONF[placeholder]["plugins"]:
                            found = False
                if found:
                    final_plugins.append(plugin)
            plugins = final_plugins
        return plugins
    
    def get_text_enabled_plugins(self, placeholder):
        plugins = self.get_all_plugins(placeholder)
        final = []
        for plugin in plugins:
            if plugin.text_enabled:
                final.append(plugin)
        return final

    def get_plugin(self, name):
        """
        Retrieve a plugin from the cache.
        """
        self.discover_plugins()
        return self.plugins[name]


plugin_pool = PluginPool()

