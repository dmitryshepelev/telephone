from django import template
from django.utils import safestring

register = template.Library()


@register.filter(name='ng')
def angularify(value):
	"""
	Filter to rule out the Django and Angular templates conflict
	:param value: string of angular value to parse
	:return: angular expression string
	"""
	return safestring.mark_safe('{{%s}}' % value)