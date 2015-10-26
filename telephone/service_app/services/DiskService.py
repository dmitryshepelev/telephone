import json
import requests
from telephone import settings
from telephone.classes.File import File
from telephone.classes.ServiceResponse import ServiceResponse
from telephone.service_app.services.LogService import LogService, Code


logger = LogService()


class DiskService():
	def __init__(self, token):
		self.__host_url = settings.API_URLS['disk']['host']
		self.__file_download_link_url = settings.API_URLS['disk']['file_download_link']
		self.__file_upload_link_url = settings.API_URLS['disk']['file_upload_link']
		self.__files_info_url = settings.API_URLS['disk']['files_info']
		self.__create_folder_url = settings.API_URLS['disk']['create_folder']

		self.__token = token
		self.__headers = {
			'Content-Type': 'application/json',
			'Authorization': 'OAuth %s' % self.__token
		}

		self.__default_folder = settings.DISK_UPLOAD_FOLDER

	@property
	def default_folder(self):
		"""
		Getter of __upload_folder
		:return: upload folder
		"""
		return self.__default_folder

	@default_folder.setter
	def default_folder(self, value):
		"""
		Setter of upload folder
		:param value: value to set
		"""
		self.__default_folder = value

	def __get_upload_link(self, filename, folder_name=None, overwrite=True):
		"""
		Get url to upload file
		:param filename: name of the file to upload
		:param folder_name: name of the folder
		:param overwrite: overwrite file flag. Default value - True
		:return: {str} link
		"""
		path = '{folder_name}/{filename}'.format(folder_name=folder_name or self.__default_folder, filename=filename)
		url = '{host}{method}{path}&overwrite={overwrite}'.format(host=self.__host_url, method=self.__file_upload_link_url, path=path, overwrite=str(overwrite).lower())

		response = requests.get(url, headers=self.__headers)
		content = json.loads(response.content)

		if response.ok:
			return content['href']

		logger.error(Code.GET_UPLOAD_LINK_ERR, data=content, status_code=response.status_code)
		return None

	def get_download_link(self, filename, folder_name=None):
		"""
		Get url to download file
		:param filename: filename
		:param folder_name: folder name
		:return: {str} link
		"""
		if not folder_name:
			folder_name = self.__default_folder

		path = '{folder_name}/{filename}'.format(folder_name=folder_name, filename=filename)
		url = '{host}{method}{path}'.format(host=self.__host_url, method=self.__file_download_link_url, path=path)

		response = requests.get(url, headers=self.__headers)
		content = json.loads(response.content)

		if response.ok:
			return content['href']

		logger.error(Code.GET_DOWNLOAD_LINK_ERR, data=content, status_code=response.status_code)
		return None

	def create_folder(self, folder_name=None):
		"""
		Create folder
		:param folder_name: name
		:return: folder_name
		"""
		if not folder_name:
			folder_name = self.__default_folder

		url = '{host}{method}{folder_name}'.format(host=self.__host_url, method=self.__create_folder_url, folder_name=folder_name)

		response = requests.put(url, headers=self.__headers)
		if response.ok or response.status_code == 409:
			# if folder created or already exist, return folder name
			return folder_name

		logger.error(Code.CREATE_FOLDER_ERR, data=json.loads(response.content), message=folder_name, status_code=response.status_code)
		return None

	def upload_file(self, file_instance, folder_name=None):
		"""
		Upload file to Disk
		:param file_instance: file instance
		:param folder_name: folder name
		:return: File instance
		"""
		folder_name = self.create_folder(folder_name)
		if not folder_name:
			return None

		upload_link = self.__get_upload_link(folder_name, file_instance.filename)
		if not upload_link:
			return None

		# upload file
		response = requests.put(upload_link, file_instance.content)
		if response.ok:
			return ServiceResponse(True, data=file_instance)

		logger.error(Code.UPLOAD_FILE_ERR, data=json.loads(response.content), status_code=response.status_code)
		return None

	def download_file(self, download_link):
		"""
		Download file from Disk
		:param download_link: link to download file
		:return: File instance
		"""
		response = requests.get(download_link)
		if response.ok:
			return File(response.content)

		logger.error(Code.DOWNLOAD_FILE_ERR, data=json.loads(response.content), status_code=response.status_code)
		return None