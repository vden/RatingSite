from django.db import models

from django.contrib.auth.models import User
from feeds.models import IndexedBlog

class TakeRequest(models.Model):
	author = models.ForeignKey(User)
	blog = models.ForeignKey(IndexedBlog)
	date = models.DateTimeField(u"Request date", auto_now=True)
	description = models.TextField(u"Request")	
