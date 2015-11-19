from unittest import TestCase
import datetime
from django.template import Context
from django.template.loader import get_template
from telephone.classes.MailMessage import MailMessage


class TestMailMessage(TestCase):
	def setUp(self):
		self.sender = 'info@web-tel.ru'
		self.subject = 'test message'
		self.template = 'mail_tmpl_subscribe_extended.html'
		self.context = Context({'username': 'test_user', 'expiration_date': datetime.datetime.now()})
		self.destination = 'dmitry.shepelev.ydx@yandex.ru'  # 'talyan-290@ya.ru'
		self.template_length = len(get_template(self.template).render(self.context).encode('cp1251'))
		self.mail_message = MailMessage(self.sender, self.subject, self.template, self.context, self.destination)

	def test_sender(self):
		self.assertEqual(self.mail_message.sender, self.sender)

	def test_destination(self):
		self.assertEqual(self.mail_message.destination, [self.destination])

	def test_content(self):
		self.assertEqual(len(self.mail_message.content), self.template_length)

	def test_subject(self):
		self.assertEqual(self.mail_message.subject, self.subject)

	def test_get_message(self):
		self.assertEqual(len(self.mail_message.get_message()), 467 + len(self.subject) + self.template_length)

	def test_send(self):
		self.assertEquals(self.mail_message.send(), True)
		self.assertEquals(self.mail_message.send(smtp='herax'), False)