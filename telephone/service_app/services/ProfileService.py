from django.contrib.auth.models import User
from telephone import settings
from telephone.classes.ServiceResponse import ServiceResponse
from telephone.classes.models.UserProfileModel import UserProfile


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
			user_profile = UserProfile.objects.create(profile_email='%s@%s' % (data['login'], settings.DOMAIN), profile_password=data['password'], uid=data['uid'], token=data['token'], user_key=data['userKey'], secret_key=data['secretKey'], user_id=user.id)
			user_profile.save()
			return ServiceResponse(True)
		except Exception as e:
			return ServiceResponse(False, e)
