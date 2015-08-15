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

	# def get_incoming(self):
	# 	return self.__incoming
	#
	# def get_status(self):
	# 	return self.__status
	#
	# def get_time(self):
	# 	return self.__time
	#
	# def get_from(self):
	# 	return self.__from
	#
	# def get_responder(self):
	# 	return self.__responder
	#
	# def get_call_time(self):
	# 	return self.__call_time
	#
	# def get_talk_time(self):
	# 	return self.__talk_time
	#
	# def get_record_id(self):
	# 	return self.__record_id