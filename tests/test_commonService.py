from unittest import TestCase
import datetime
from telephone.service_app.services.CommonService import CommonService

__author__ = 'DShepelev'


class TestCommonService(TestCase):
	def test_add_months(self):
		date = datetime.datetime(2015, 10, 30, 20, 0, 0)
		self.assertEquals(CommonService.add_months(date, 1), datetime.datetime(2015, 11, 30, 20, 0, 0))

		self.assertEquals(CommonService.add_months(date, 4), datetime.datetime(2016, 02, 29, 20, 0, 0))

	def test_get_params_string(self):
		params = {'a': 'foo', 'b': 'bar', 'c': 42}
		self.assertEqual(CommonService.get_params_string(params), 'a=foo&b=bar&c=42')

		params_1 = {}
		self.assertEqual(CommonService.get_params_string(params_1), '')