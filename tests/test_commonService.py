from unittest import TestCase
import datetime
from telephone.service_app.services.CommonService import CommonService


class TestCommonService(TestCase):
	def test_add_months(self):
		"""
		Test two cases of add_month method
		"""
		date = datetime.datetime(2015, 10, 30, 20, 0, 0)
		self.assertEquals(CommonService.add_months(date, 1), datetime.datetime(2015, 11, 30, 20, 0, 0))
		self.assertEquals(CommonService.add_months(date, 4), datetime.datetime(2016, 02, 29, 20, 0, 0))

	def test_get_params_string(self):
		"""
		Test for get_params_string method
		"""
		params = {'a': 'foo', 'b': 'bar', 'c': 42}
		self.assertEqual(CommonService.get_params_string(params), 'a=foo&b=bar&c=42')
		params_1 = {}
		self.assertEqual(CommonService.get_params_string(params_1), '')

	def test_is_dates_equals(self):
		"""
		Test for is_dates_equals
		"""
		date = datetime.datetime(2015, 10, 30, 20, 0, 0)

		# Dates are the same
		date2 = datetime.datetime(2015, 10, 30, 20, 0, 0)
		self.assertEquals(CommonService.is_dates_equals(date, date2, False), True)

		# The first date is less in 1 min
		date3 = datetime.datetime(2015, 10, 30, 20, 1, 0)
		self.assertEquals(CommonService.is_dates_equals(date, date3, False), True)

		# The first date is less in 2 min
		date4 = datetime.datetime(2015, 10, 30, 20, 2, 0)
		self.assertEquals(CommonService.is_dates_equals(date, date4, False), False)

		# The first date is less in 1 hour
		date5 = datetime.datetime(2015, 10, 30, 21, 0, 0)
		self.assertEquals(CommonService.is_dates_equals(date, date5, False), False)

		# Comparison with seconds
		date6 = datetime.datetime(2015, 10, 30, 20, 0, 3)
		self.assertEquals(CommonService.is_dates_equals(date, date6, True), True)

		# Comparison with seconds
		date7 = datetime.datetime(2015, 10, 30, 20, 0, 4)
		self.assertEquals(CommonService.is_dates_equals(date, date7, True), False)