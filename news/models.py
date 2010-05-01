from django.db import models
import fts
from tinymce import models as tinymce_models
from django.utils.translation import ugettext_lazy as _

class News(fts.SearchableModel):
    title = models.CharField(_("Title"), max_length=1023, blank=False, null=False)
    description = models.TextField(_("Short description"), blank=True, null=True)
    body = tinymce_models.HTMLField()

    date = models.DateTimeField(_("Publishing date"), blank=False, null=False)
    published = models.BooleanField(_("Published"))

    photo = models.ImageField(_("Photo"), blank=True, null=True, upload_to="photos/%Y/%m/%d")

    objects = fts.SearchManager( fields=('title','description', 'body') )

    def __unicode__(self):
        return self.title
    str = __unicode__

    def get_absolute_url(self):
        return u"/news/%s/"%self.id
    
    @classmethod
    def last(cls, count=10):
	return News.objects.order_by('-date').filter(published=True)[:count]
