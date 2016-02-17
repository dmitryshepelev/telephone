import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
import pytz

from telephone.classes.ServiceResponse import ServiceResponse
from telephone.main_app.models import Call, Callee, SubscribeTransaction, TransactionStatus, ProfileRequestTransaction, \
	RegisteredCallback, IncomingInfo
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
				return ServiceResponse(False, data=callee, message=str(e))
			return ServiceResponse(True, data=callee)

	@staticmethod
	def create_call(call_record, userprofile):
		"""
		Create call entity
		:param call_record: Call instance
		:param userprofile: UserProfile instance
		:return: Call instance
		"""
		if (isinstance(call_record.destination, str) or isinstance(call_record.destination, unicode)) and 'w00e' in call_record.destination:
			call_record.destination = call_record.destination[4:]

		if (isinstance(call_record.sip, str) or isinstance(call_record.sip, unicode)) and 'w00e' in call_record.sip:
			call_record.sip = call_record.sip[4:]

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
				user_profile=userprofile,
				callee=result.data,
				call_type=call_record.call_type
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
			logger.error(Code.GET_CALL_ERR, props=kwargs, message=str(e))
			return None

	@staticmethod
	def create_subscr_transaction(user, params):
		"""
		Creates new Subscribe transaction
		:param user: current user
		:param params: transaction params
		:return: SubscribeTransaction instance
		"""
		try:
			subscr = SubscribeTransaction(
				transact_id=params['label'],
				receiver=params['receiver'],
				form_comments=params['form_comment'],
				short_dest=params['short_dest'],
				quickpay_form=params['quickpay_form'],
				targets=params['targets'],
				sum=params['sum'],
				payment_type=params['paymentType'],
				duration=params['duration'],
				expiration_date=None,
				user_profile=user.userprofile,
				status=TransactionStatus.objects.get(pk=1)
			)
			subscr.save()
			return subscr
		except Exception as e:
			logger = LogService()
			logger.error(Code.CREATE_SUBSCR_TRANSACTION_ERR, props=params, message=str(e))
			return None

	@staticmethod
	def get_transact(transact_id):
		"""
		Get an existing transact by its id
		:param transact_id: transact_id
		:return: Transact instance
		"""
		try:
			from telephone.classes.view_models.SubscribeTransaction import SubscribeTransactionVM
			from telephone.classes.view_models.ProfileRequestTransaction import ProfileRequestTransactionVM

			try:
				return SubscribeTransactionVM(SubscribeTransaction.objects.get(transact_id=transact_id))
			except ObjectDoesNotExist as e:
				return ProfileRequestTransactionVM(ProfileRequestTransaction.objects.get(transact_id=transact_id))

		except Exception as e:
			logger = LogService()
			logger.error(Code.GET_TRANSACT_ERR, transact_id=transact_id, message=str(e))
			return None

	@staticmethod
	def create_profile_request_transact(profile_request):
		"""
		Create a new profile request transaction
		:param profile_request: ProfileRequest instance
		:return: created ProfileRequestTransaction instance
		"""
		profile_request_transact = None
		try:
			profile_request_transact = ProfileRequestTransaction(
				transact_id=profile_request.transact_id,
				creation_date=profile_request.creation_date,
				email=profile_request.email,
				username=profile_request.login,
				status=TransactionStatus.objects.get(pk=1)
			)
			profile_request_transact.save()
			return profile_request_transact
		except Exception as e:
			logger = LogService()
			logger.error(Code.CREATE_SUBSCR_TRANSACTION_ERR, data=profile_request_transact, message=str(e))
			return None

	@staticmethod
	def register_callback(user_profile, caller, destination):
		"""
		Register callback in database
		:param user_profile: user's profile instance
		:param caller: callback caller
		:param destination: callback destination
		:return:
		"""
		callback = None
		try:
			callback = RegisteredCallback(caller=caller, destination=destination, user_profile=user_profile)
			callback.save()
			return callback
		except Exception as e:
			logger = LogService()
			logger.error(Code.REGISTER_CALLBACK_ERR, data=callback, message=str(e))
		return None

	@staticmethod
	def create_incoming_info(caller_id, called_did, call_start, script_guid):
		"""
		Creates incoming info
		:param caller_id:
		:param called_did:
		:param call_start:
		:param script_guid:
		:return:
		"""
		incoming_info = None
		try:
			expiration_date = call_start + datetime.timedelta(minutes=2)
			incoming_info = IncomingInfo(caller_id=caller_id, call_start=call_start, called_did=called_did, expiration_date=expiration_date, script_id=script_guid)
			incoming_info.save()
			return incoming_info
		except Exception as e:
			logger = LogService()
			logger.error(Code.INCOMING_INFO_ERR, data=incoming_info, message=str(e))
		return None

	@staticmethod
	def get_incoming_info(script_guid):
		"""
		Get incoming info
		:param script_guid:
		:return:
		"""
		incoming_info = IncomingInfo.objects.filter(script_id=script_guid).order_by('-call_start').first()

		if not incoming_info:
			return None

		delta = (incoming_info.expiration_date.replace(tzinfo=pytz.utc).replace(tzinfo=None) - datetime.datetime.now(tz=pytz.timezone(pytz.country_timezones['RU'][1])).replace(tzinfo=None))
		if delta.days == 0 and delta.seconds < 180:
			return incoming_info

		return None