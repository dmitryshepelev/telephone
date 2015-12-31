# coding=utf-8
from django import template
from telephone.service_app.services.CommonService import CallsConstants

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


@register.filter(name='call_state_icon')
def cal_state_icon(value):
	"""
	Return icomoon class
	:param value: call instance
	:return: class
	"""
	icon = 'icon-{type}'.format(type=('arrow-down' if value.call_type == CallsConstants.INCOMING else ('arrow-up' if value.call_type == CallsConstants.COMING else 'loop')))
	status = 'text-{status}'.format(status=('success' if value.disposition == CallsConstants.ANSWERED else 'error'))

	return icon + ' ' + status


@register.filter(name='is_call_answered')
def is_call_answered(call, prop=None):
	"""
	Return '-' value if call isn't answered else value of prop
	:param call: call
	:param prop: prop name
	"""

	if call.disposition != 'answered':
		return '-' if prop else False

	return (call.__dict__[prop] if call.__dict__[prop] is not None else '-') if prop else True