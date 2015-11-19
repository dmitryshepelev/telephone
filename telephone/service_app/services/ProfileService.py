import datetime

from django.contrib.auth.models import User

from telephone.classes.ServiceResponse import ServiceResponse
from telephone.main_app.models import UserProfile, ProfileRequestTransaction
from telephone.service_app.services.CommonService import CommonService


class ProfileService():
	def __init__(self):
		pass

	@staticmethod
	def create_profile(data):
		"""
		Creates a new user and userProfile
		:param data: NewUserForm data instance
		:return: ServiceResponse
		"""
		try:
			user = User.objects.create_user(username=data['userName'], email=data['userEmail'], password=data['userPassword'])
			user.save()
			user_profile = UserProfile.objects.create(profile_email='%s', profile_password=data['password'], uid=data['uid'], token=data['token'], user_key=data['userKey'], secret_key=data['secretKey'], user_id=user.id, customer_number=data['customerNumber'])
			user_profile.save()
			return ServiceResponse(True)
		except Exception as e:
			return ServiceResponse(False, e.message)

	@staticmethod
	def extend_subscription(user_profile, duration):
		"""
		Extend profile subscription
		:param user: User instance
		:param duration: {int} duration in month
		:return:
		"""
		user_profile = UserProfile.objects.get(pk=user_profile.pk)

		if user_profile.date_subscribe_ended:
			new_date = CommonService.add_months(user_profile.date_subscribe_ended, duration)
		else:
			new_date = CommonService.add_months(datetime.datetime.now(), duration)

		user_profile.date_subscribe_ended = new_date
		user_profile.save()