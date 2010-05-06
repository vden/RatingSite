from django.db import models

from django.contrib.auth.models import User
from feeds.models import IndexedBlog

from django_openid_auth.models import UserOpenID
from django.core.urlresolvers import reverse

class TakeRequest(models.Model):
	author = models.ForeignKey(User)
	blog = models.ForeignKey(IndexedBlog)
	date = models.DateTimeField(u"Request date", auto_now=True)
	description = models.TextField(u"Request")	

	def author_name(self):
		uoid = UserOpenID.objects.filter(user=self.author)
		if not len(uoid): return u""
		else:
			return uoid[0].claimed_id      

	def approve_link(self):
		return """<a href="%s"><span style="color:green">Approve</span></a>"""%reverse("approve-request", args=[self.id,])
	approve_link.allow_tags = True

	def reject_link(self):
       		return """<a href="%s"><span style="color:red">Reject</span></a>"""%reverse("reject-request", args=[self.id,])
	reject_link.allow_tags = True
