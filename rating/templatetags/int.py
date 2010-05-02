from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter
@stringfilter
def int_filter(value):
	return str( int( float( value ) ) )
