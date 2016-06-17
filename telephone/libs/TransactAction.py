from abc import ABCMeta, abstractmethod


class TransactAction(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def confirm(self, **kwargs):
		pass

	@abstractmethod
	def cancel(self, **kwargs):
		pass

	@abstractmethod
	def archive(self, **kwargs):
		pass