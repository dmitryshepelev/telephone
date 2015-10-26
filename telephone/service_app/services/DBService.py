from django.core.exceptions import ObjectDoesNotExist
import pytz

from telephone.classes.ServiceResponse import ServiceResponse
from telephone.main_app.models import Call, Callee
from telephone.service_app.services.LogService import LogService, Code


class DBService():
	def __init__(self):
		pass

	@staticmethod
	def create_callee(callee):
		"""
		Create a callee entity if not exist. Else update date of first call
		:param callee: Callee instance
		:return: Callee instance
		"""
		try:
			# Get existing callee entity by its phone number
			exs_callee = Callee.objects.get(sip=callee.sip)
			# check if existing callee first call date over current callee first call date
			# If true that means current call of callee was before existing and existing needs to be updated with new date
			if exs_callee.first_call_date.replace(tzinfo=pytz.utc).replace(tzinfo=None) > callee.first_call_date:
				exs_callee.first_call_date = callee.first_call_date
				exs_callee.save()
			# Else just return existing callee
			return ServiceResponse(True, data=exs_callee)
		except ObjectDoesNotExist as e:
			# Create a new callee
			try:
				callee.save()
			except Exception as e:
				# Callee isn't created
				return ServiceResponse(False, data=callee, message=e.message)
			return ServiceResponse(True, data=callee)

	@staticmethod
	def create_call(call_record, userprofile):
		"""
		Create call entity
		:param call_record: Call instance
		:param userprofile: UserProfile instance
		:return: Call instance
		"""
		callee = Callee(
			sip=call_record.sip,
			description=call_record.description,
			first_call_date=call_record.date
		)
		# create Callee entity or ensure it exist
		result = DBService.create_callee(callee)
		if result.is_success:
			call = Call(
				call_id=call_record.call_id,
				date=call_record.date,
				destination=call_record.destination,
				disposition=call_record.disposition,
				bill_seconds=call_record.bill_seconds,
				cost=call_record.cost,
				bill_cost=call_record.bill_cost,
				currency=call_record.currency,
				is_answered=call_record.is_answered,
				user_profile=userprofile,
				callee=result.data
			)
			# create Call Instance
			try:
				call.save()
			except Exception as e:
				# Call isn't created
				return ServiceResponse(False, data=call, message=e.message)
			return ServiceResponse(True, data=call)
		# Callee isn't created
		return ServiceResponse(False, data=result.data, message=result.message)

	@staticmethod
	def get_call(**kwargs):
		"""
		Get Call entity by prop names
		:param kwargs: prop names
		:return: Call entity
		"""
		try:
			return Call.objects.get(**kwargs)
		except Exception as e:
			logger = LogService()
			logger.error(Code.GET_CALL_ERR, props=kwargs, message=e.message)
			return None

	@staticmethod
	def update_call(call, **kwargs):
		"""
		Update call entity
		:param call: call db instance
		:param kwargs: values to update
		"""
		for key, value in kwargs.iteritems():
			if key in call.keys():
				call[key] = value
		call.save()