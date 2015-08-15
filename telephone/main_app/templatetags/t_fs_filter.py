# coding=utf-8
from django import template
import math
from django.utils import safestring

register = template.Library()


@register.filter(name='t_fs')
def from_second(value):
	"""
	Convert second to min and sec string value
	:param value: sec value
	:return: min and sec string value
	"""
	value = int(value)
	minutes = math.floor(value / 60)
	seconds = value - minutes * 60
	return safestring.mark_safe('%s%s' % ('%s%s' % (int(minutes), ' мин ') if minutes > 0 else '', '%s%s' % (int(seconds), ' сек')))