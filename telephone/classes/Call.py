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


class CallATS():
	def __init__(self, data):
		self.call_id = data['call_id']
		self.sip = data['sip']
		self.date = datetime.datetime.strptime(data['callstart'], '%Y-%m-%d %H:%M:%S')
		self.destination = data['destination']
		self.disposition = data['disposition']
		self.seconds = data['seconds']
		self.clid = data['clid']


class CallRecord():
	def __init__(self, call, callATS):
		self.call_id = callATS.call_id
		self.sip = callATS.sip
		self.date = callATS.date
		self.destination = call.destination
		self.description = call.description
		self.disposition = call.disposition
		self.bill_seconds = call.bill_seconds
		self.cost = call.cost
		self.bill_cost = call.bill_cost
		self.currency = call.currency