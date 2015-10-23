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

	def __get_upload_link(self, folder_name, filename, overwrite=True):
		"""
		Get url to upload file
		:param folder_name: name of the folder
		:param overwrite: overwrite file flag. Default value - True
		:return: {str} link
		"""
		path = '{folder_name}/{filename}'.format(folder_name=folder_name, filename=filename)
		url = '{host}{method}{path}&overwrite={overwrite}'.format(host=self.__host_url, method=self.__file_upload_link_url, path=path, overwrite=str(overwrite).lower())
		response = requests.get(url, headers=self.__headers)
		if response.ok:
			return json.loads(response.content)['href']
		logger.error(Code.DGULER, data=response.content, status_code=response.status_code)
		return False

	def get_download_link(self, filename, folder_name=None):
		"""
		Get url to download file
		:param filename: filename
		:param folder_name: folder name
		:return: {str} link
		"""
		path = '{folder_name}/{filename}'.format(folder_name=folder_name, filename=filename)
		url = '{host}{method}{path}'.format(host=self.__host_url, method=self.__file_download_link_url, path=path)
		response = requests.get(url, headers=self.__headers)
		if response.ok:
			return ServiceResponse(True, data=json.loads(response.content)['href'])
		logger.error(Code.DGDLER, data=response.content, status_code=response.status_code)
		return ServiceResponse(False, data=response.content, status_code=response.status_code)

	def create_folder(self, folder_name):
		"""
		Create folder
		:param folder_name: name
		:return:
		"""
		if not folder_name:
			raise ValueError

		url = '{host}{method}{folder_name}'.format(host=self.__host_url, method=self.__create_folder_url, folder_name=folder_name)

		response = requests.put(url, headers=self.__headers)

		if response.ok or response.status_code == 409:
			return ServiceResponse(True, data=folder_name, status_code=response.status_code)
		logger.error(Code.DFCRER, data=json.loads(response.content), message=folder_name, status_code=response.status_code)
		return ServiceResponse(False, data=json.loads(response.content), status_code=response.status_code)

	def upload_file(self, file, folder_name=None):
		"""
		Upload file to Disk
		:param file: file instance
		:param folder_name: folder name
		:return:
		"""
		result = self.create_folder(folder_name)

		if result.is_success:
			upload_link = self.__get_upload_link(result.data, file.filename)
			if upload_link:
				response = requests.put(upload_link, file.content)
				if response.ok:
					return ServiceResponse(True, data=file.filename)
				else:
					logger.error(Code.DFUPER, data=json.loads(response.content), status_code=response.status_code)
		return ServiceResponse(False)

	def download_file(self, download_link):
		"""
		Download file from Disk
		:param download_link: link to download file
		:return: File instance
		"""
		response = requests.get(download_link)
		if response.ok:
			return ServiceResponse(True, data=File(response.content))
		logger.error(Code.DFDPER, data=json.loads(response.content), status_code=response.status_code)
		return ServiceResponse(False)