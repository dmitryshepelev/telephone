from unittest import TestCase
import datetime
from telephone.service_app.services.ApiService import ApiService


class TestApiService(TestCase):
	def test_generate_email_password(self):
		email_id = '123'
		date_text = datetime.datetime.now().strftime('%d%m%y')
		self.assertEquals(ApiService.generate_email_password(email_id), 'wt%sp%s' % (date_text, email_id))