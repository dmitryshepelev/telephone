# coding=utf-8
import time
import datetime


class Call():
	def __init__(self, arr):
		self.incoming = True if 'входящий' == arr[0] else False if 'исходящий' == arr[0] else None
		self.status = True if 'отвечен' == arr[1] else False
		self.time = datetime.datetime.strptime(arr[2], '%d.%m.%Y %H:%M:%S')
		self.fromNumber = arr[4]
		self.responder = arr[6]
		self.callTime = int(arr[7]) if arr[7] else 0
		self.talkTime = int(arr[8]) if arr[8] else 0
		self.recordId = arr[11]