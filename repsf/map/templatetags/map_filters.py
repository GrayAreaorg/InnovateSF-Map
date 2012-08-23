from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.filter
@stringfilter
def replace(value, arg):
	args = arg.split(',')
	return value.replace(args[0], args[1])