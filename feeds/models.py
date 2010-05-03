from django.db import models
from core.accounts import Profile
import string
from django.contrib.auth.models import User

class IndexedBlog(models.Model):
	url = models.URLField(u"Blog URL", verify_exists=False, max_length=1024)
	owner = models.ForeignKey(User, verbose_name=u"Blog owner", blank=True, null=True)
	
	def __unicode__(self):
		return self.url
	
class StatCategory(models.Model):
	name = models.CharField(u"Category name", max_length=256)
	# links, links24, visits etc
	description = models.CharField(u"Category description", max_length=1024)
	category_weight = models.FloatField(u"Category weight", default = 1.0)

	def __unicode__(self):
		return self.name
	
class IndexedArticle(models.Model):
	blog =  models.ForeignKey(IndexedBlog, verbose_name=u"Blog")
	title = models.CharField(u"Article title", max_length=10000)
	link = models.URLField(u"Article URL", verify_exists=False, max_length=10000)
	pubdate = models.DateTimeField(u"Publication date")

	def __unicode__(self):
		slist = StatAtom.objects.filter(article = self)
		l = [ "%s: %s"%(x.category.name, x.value) for x in slist ]
		
		return u"%s: (%s)"%(self.title, string.join(l, "; "))

class StatAtom(models.Model):
	category = models.ForeignKey(StatCategory, verbose_name=u"Category name")
	article = models.ForeignKey(IndexedArticle, verbose_name=u"Article")
	value = models.FloatField(u"Stat value", default=0)
#	updated = models.DateTimeField(u"Last updated")
	
	def update_value(self, v, d):
		if not self.updated or d > self.updated:
			self.value = self.value + float(v)
			self.updated = d

			self.save()
