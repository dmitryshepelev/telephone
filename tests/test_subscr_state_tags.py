# coding=utf-8
from unittest import TestCase

from telephone.my_app.templatetags import ending_resolver


class TestEndingResolver(TestCase):
	def test_ending_resolver_one(self):
		self.assertEqual(ending_resolver(1), 'день')

	def test_ending_resolver_tree(self):
		self.assertEqual(ending_resolver(3), 'дня')

	def test_ending_resolver_seven(self):
		self.assertEqual(ending_resolver(7), 'дней')

	def test_ending_resolver_zero(self):
		self.assertEqual(ending_resolver(0), 'дней')