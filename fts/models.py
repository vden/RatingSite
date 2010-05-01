"""
Full Text Search Framework
"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from fts.settings import *

if FTS_CONFIGURE_ALL_BACKENDS or FTS_BACKEND.startswith('simple://'):
    class Word(models.Model):
        word = models.CharField(unique=True, db_index=True, blank=False, max_length=100)
        
        def __unicode__(self):
            return u"%s" % (self.word)
    
    class Index(models.Model):
        word = models.ForeignKey(Word)
        weight = models.IntegerField()
        namespace = models.CharField(max_length=10, db_index=True, null=True, blank=True)
        
        content_type = models.ForeignKey(ContentType)
        object_id = models.PositiveIntegerField(db_index=True)
        content_object = generic.GenericForeignKey('content_type', 'object_id')
        
        def __unicode__(self):
            return u'%s [%s]' % (self.content_object, self.word.word)
