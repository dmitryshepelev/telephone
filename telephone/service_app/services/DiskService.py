import json
import requests
from telephone import settings


class DiskService():
	def __init__(self, token):
		self.__host_url = settings.API_URLS['disk']['host']
		self.__file_download_link_url = settings.API_URLS['disk']['file_download_link']
		self.__files_info_url = settings.API_URLS['disk']['files_info']

		self.__token = token

	def get_files_info(self, limit=1000, media_type='audio', fields='"name,path,size"'):
		url = '%s%s?limit=%s&media_type=%s&fields=%s' % (self.__host_url, self.__files_info_url, limit, media_type, fields)

		api_response = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': 'OAuth %s' % (self.__token)})
		if api_response.ok:
			data = json.loads(api_response.content)
		return None