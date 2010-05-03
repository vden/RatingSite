from django.template.defaultfilters import stringfilter
from django import template

from django.core.urlresolvers import reverse

from feeds.models import *
from rating.models import *

register = template.Library()

@register.filter
@stringfilter
def int_filter(value):
	if value=="": value="-1.0"
	return str( int( float( value ) ) )

@register.simple_tag
def table_value(value, blog_id, category_id):
	cats = ["comments", "commenters", "links"]

	r = u"""<a href="%s">%d</a>"""%(reverse('list-articles', args=[blog_id, cats[int(category_id)] ] ), int( float( value ) ) )

	return r
