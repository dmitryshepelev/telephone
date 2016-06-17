# coding=utf-8
import inspect
import datetime
from telephone import settings
from telephone.libs.MailMessage import MailMessage
from telephone.libs.TransactAction import TransactAction
from telephone.service_app.services.CommonService import CommonService
from telephone.service_app.services.LogService import LogService, Code
from telephone.service_app.services.ProfileService import ProfileService


class SubscribeTransactionVM(TransactAction):
	def __init__(self, transact):
		super(SubscribeTransactionVM, self).__init__()
		self.__transact = transact
		self.__logger = LogService()

	def archive(self, **kwargs):
		"""
		Execute to archive transaction
		:return: transact
		"""
		self.__transact.is_archive = not self.__transact.is_archive
		return self.__save()

	def confirm(self, **kwargs):
		"""
		Execute confirm transaction
		:return: transact
		"""
		self.__transact.status_id = 2
		self.__transact.expiration_date = CommonService.add_months(datetime.datetime.now(), self.__transact.duration)
		return self.__save(self.__extend_subscription)

	def cancel(self, **kwargs):
		"""
		Change transact status to cancel
		:return: transact
		"""
		self.__transact.status_id = 3
		return self.__save()

	def __extend_subscription(self, *args):
		"""
		Extend profile subscription and send e-mail
		:param args:
		"""
		ProfileService.extend_subscription(self.__transact.user_profile, self.__transact.duration)

		message = MailMessage(settings.INFO_EMAIL, 'Продление подписки', 'mail_tmpl_subscribe_extended.html', {
			'username': self.__transact.user_profile.user.username,
			'expiration_date': self.__transact.user_profile.date_subscribe_ended
		}, self.__transact.user_profile.user.email)
		message.send()

	def __save(self, on_success=None):
		"""
		Save entity changes
		:param on_success: callback on successful changes
		:return: True if saving executed success or False if exception has been raised
		"""
		try:
			self.__transact.save()
			if on_success and hasattr(on_success, '__call__'):
				on_success(self.__transact)
			return True
		except Exception as e:
			self.__logger.error(Code.SAVE_ENTITY_ERR, action=inspect.stack()[1][3], transact_id=self.__transact.transact_id, message=str(e))
			return False

	@property
	def transact_id(self):
		"""
		Getter of __transact_id
		:return: transact_id value
		"""
		return self.__transact.transact_id

	@property
	def sum(self):
		"""
		Getter of __sum
		:return: sum value
		"""
		return self.__transact.sum

	@property
	def payment_type(self):
		"""
		Getter of __payment_type
		:return: payment_type value
		"""
		return self.__transact.payment_type

	@property
	def duration(self):
		"""
		Getter of __duration
		:return: duration value
		"""
		return '{value} мес'.format(value=self.__transact.duration)

	@property
	def username(self):
		"""
		Getter of __username
		:return: username value
		"""
		return self.__transact.user_profile.user.username

	@property
	def creation_date(self):
		"""
		Getter of __creation_date
		:return: creation_date value
		"""
		return self.__transact.creation_date

	@property
	def status_id(self):
		"""
		Getter of __status_id
		:return: status_id value
		"""
		return self.__transact.status_id

	@property
	def status_value(self):
		"""
		Getter of __status_value
		:return: status_value value
		"""
		return self.__transact.status.value

	@property
	def is_archive(self):
		"""
		Getter of __is_archive
		:return: is_archive value
		"""
		return self.__transact.is_archive