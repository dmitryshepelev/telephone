# coding=utf-8
from django import template

register = template.Library()


@register.filter(name='call_state_localize')
def call_state_localize(value):
	"""
	Localize current call state to RU
	:param value: call state value
	:return: localized string value
	"""
	if value == 'answered':
		return 'Отвечен'
	elif value == 'busy':
		return 'Занято'
	elif value == 'cancel':
		return 'Отменен'
	elif value == 'no answer':
		return 'Нет ответа'
	elif value == 'failed':
		return 'Неудачный'
	elif value == 'no money':
		return 'Нет средств'
	elif value == 'unallocated number':
		return 'Номер не существует'
	elif value == 'no limit' or value == 'no money, no limit':
		return 'Превышен лимит'
	elif value == 'no day limit':
		return 'Превышен дневной лимит'
	elif value == 'line limit':
		return 'Превышен лимит линии'
	else:
		return ''