# coding=utf-8
import time
import datetime


class Call():
	def __init__(self, data):
		self.call_id = data['id']
		self.sip = data['sip']
		self.date = datetime.datetime.strptime(data['callstart'], '%Y-%m-%d %H:%M:%S')
		self.destination = data['to']
		self.description = data['description']
		self.disposition = data['disposition']
		self.bill_seconds = data['billseconds']
		self.cost = data['cost']
		self.bill_cost = data['billcost']
		self.currency = data['currency']


class CallPBX():
	def __init__(self, data):
		self.call_id = data['call_id']
		self.sip = data['sip']
		self.date = datetime.datetime.strptime(data['callstart'], '%Y-%m-%d %H:%M:%S')
		self.destination = data['destination']
		self.disposition = data['disposition']
		self.seconds = data['seconds']
		self.clid = data['clid']


class CallRecord():
	def __init__(self, call_common, call_pbx):
		self.call_id = call_pbx.call_id
		self.sip = call_pbx.sip
		self.date = call_pbx.date
		self.destination = call_common.destination
		self.description = call_common.description
		self.disposition = call_common.disposition
		self.bill_seconds = call_common.bill_seconds
		self.cost = call_common.cost
		self.bill_cost = call_common.bill_cost
		self.currency = call_common.currency