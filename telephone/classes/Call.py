# coding=utf-8
import time
import datetime


class Call():
	def __init__(self, data):
		if isinstance(data, dict):
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
		else:
			self.call_id = data[0]
			self.sip = data[1]
			self.date = datetime.datetime.strptime(data[2], '%Y-%m-%d %H:%M:%S')
			self.destination = data[4]
			self.description = data[5]
			self.disposition = data[6]
			self.bill_seconds = data[7]
			self.cost = data[8]
			self.bill_cost = data[9]
			self.currency = data[10]