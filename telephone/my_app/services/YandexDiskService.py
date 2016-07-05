import json

import requests

from telephone import settings
from telephone.libs.File import File
from telephone.my_app.services.YandexService import YandexService, YandexServiceResultError


class YandexDiskServiceResultError(YandexServiceResultError):
	"""
	Yandex Disk Service result error
	"""
	pass


class YandexDiskServiceUploadError(YandexServiceResultError):
	"""
	Raises when upload error is occured
	"""
	pass


class YandexDiskServiceDownloadError(YandexServiceResultError):
	"""
	Raises when download error is occured
	"""
	pass


class YandexDiskService(YandexService):
	"""
	Yandex Disk service
	"""
	def __init__(self, yandex_profile):
		super(YandexDiskService, self).__init__(yandex_profile)

		self._default_dir_name = settings.YANDEX['disk']['default_dir_name']
		self.__host = settings.YANDEX['disk']['host']

	def _get_or_create_dir(self, dir_name = None):
		"""
		Create folder
		:return: folder_name
		"""
		dir_name = dir_name or self._default_dir_name
		method = settings.YANDEX['disk']['create_dir']

		url = '{host}{method}{dir_name}'.format(host = self.__host, method = method, dir_name = dir_name)

		response = requests.put(url, headers = self._get_request_headers())
		if response.ok or response.status_code == 409:
			# if folder created or already exist, return folder name
			return dir_name

		raise YandexDiskServiceResultError(response.status_code, response.content)

	def __get_upload_link(self, filename, dir_name = None, overwrite = True):
		"""
		Get url to upload file
		:param filename: name of the file to upload
		:param dir_name: name of the folder
		:param overwrite: overwrite file flag. Default value - True
		:return: {str} link
		"""
		method = settings.YANDEX['disk']['upload_link']

		path = '{dir_name}/{filename}'.format(dir_name = dir_name or self._default_dir_name, filename = filename)
		url = '{host}{method}{path}&overwrite={overwrite}'.format(host = self.__host, method = method, path = path, overwrite = str(overwrite).lower())

		response = requests.get(url, headers = self._get_request_headers())
		content = json.loads(response.content)

		if response.ok:
			return content['href']

		raise YandexDiskServiceResultError(response.status_code, response.content)

	def upload(self, file_instance, dir_name = None, overwrite = True):
		"""
		Upload file to the disk
		:return:
		"""
		dir_name = self._get_or_create_dir(dir_name)

		upload_link = self.__get_upload_link(file_instance.filename, dir_name, overwrite)

		# upload file
		response = requests.put(upload_link, file_instance.content)
		if not response.ok:
			raise YandexDiskServiceUploadError(response.status_code, response.content)

	def get_download_link(self, filename, dir_name = None):
		"""
		Returns link to download the file
		:param dir_name:
		:param filename:
		:return:
		"""
		method = settings.YANDEX['disk']['download_link']
		dir_name = self._get_or_create_dir(dir_name)

		path = '{dir_name}/{filename}'.format(dir_name = dir_name, filename = filename)
		url = '{host}{method}{path}'.format(host = self.__host, method = method, path = path)

		response = requests.get(url, headers = self._get_request_headers())
		content = json.loads(response.content)

		if response.ok:
			return content['href']

		raise YandexDiskServiceResultError(response.status_code, response.content)

	def download(self, link):
		"""
		Download file by link
		:return:
		"""
		response = requests.get(link)
		if response.ok:
			return File(response.content)

		raise YandexDiskServiceDownloadError(response.status_code, response.content)
