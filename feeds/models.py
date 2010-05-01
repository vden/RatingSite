from django.db import models
from core.accounts import Profile
import string

class IndexedBlog(models.Model):
	url = models.URLField(u"Blog URL", verify_exists=False, max_length=1024)
	owner = models.ForeignKey(Profile, verbose_name=u"Blog owner", blank=True, null=True)

class StatCategory(models.Model):
	name = models.CharField(u"Category name", max_length=256)
	# links, links24, visits etc
	category_weight = models.FloatField(u"Category weight", default = 1.0)

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
	value = models.FloatField(u"Stat value")
