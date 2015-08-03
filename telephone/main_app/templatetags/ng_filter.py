from django import template
from django.utils import safestring

register = template.Library()


@register.filter(name='ng')
def angularify(value):
	return safestring.mark_safe('{{%s}}' % value)