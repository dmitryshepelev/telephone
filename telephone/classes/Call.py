# coding=utf-8
import time
import datetime


class Call():
	def __init__(self, arr):
		self.call_id = arr[0]
		self.sip = arr[1]
		self.date = datetime.datetime.strptime(arr[2], '%Y-%m-%d %H:%M:%S')
		self.destination = arr[4]
		self.description = arr[5]
		self.disposition = arr[6]
		self.bill_seconds = arr[7]
		self.cost = arr[8]
		self.bill_cost = arr[9]
		self.currency = arr[10]