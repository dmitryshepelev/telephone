import time
from datetime import datetime, date
import tzlocal

import pytz

from telephone import settings


class DateTimeUtil(object):

	@staticmethod
	def check_type(value):
		"""
		Check if the value is datetime type and raise an error if not
		:param value:
		:return:
		"""
		if isinstance(value, datetime) or isinstance(value, date):
			return

		raise ValueError('Value must be a datetime instance')

	@staticmethod
	def from_timestamp(timestamp):
		"""
		Parse new Date() js object to Python DateTime
		:param timestamp:
		:return:
		"""
		return datetime.fromtimestamp(float(timestamp) / 1000.0)

	@staticmethod
	def to_timestamp(value):
		"""
		Convert datetime to timestamp
		:param value: {datetime} instance
		:return:
		"""
		DateTimeUtil.check_type(value)
		return int(time.mktime(value.timetuple()) * 1000)

	@staticmethod
	def convert_to_UTC(date):
		"""
		Set UTC timezone to date
		:param date:
		:return:
		"""
		DateTimeUtil.check_type(date)

		if date.tzinfo is None:
			local_timezone = tzlocal.get_localzone()
			local_datetime = local_timezone.localize(date, is_dst = None)
			return local_datetime.astimezone(pytz.utc)

		return date

	@staticmethod
	def to_simple_datetime_format(date):
		"""
		Represents datetime as 'YYYY-MM-dd hh:mm:ss" string
		:return:
		"""
		DateTimeUtil.check_type(date)
		return date.strftime('%Y-%m-%d %H-%M-%S')

	@staticmethod
	def equals(date_1, date_2, with_sec):
		"""
		Check if the dates are equals with error
		:param date_1: DateTime
		:param date_2: DateTime
		:param with_sec: comparison by secs
		:return: Boolean
		"""
		if with_sec:
			return abs(date_1 - date_2).seconds <= settings.TIME_CORRECTION_SEC
		return date_1.date() == date_2.date() and date_1.hour == date_2.hour and abs(date_1.minute - date_2.minute) <= settings.TIME_CORRECTION_MIN