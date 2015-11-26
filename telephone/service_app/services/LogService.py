import inspect
import logging

__logger = logging.getLogger('app_logger')


class Code():
	def __init__(self):
		pass
	# DBService codes
	GET_CALL_ERR = 'DB. GET CALL ERROR'
	UPDATE_CALL_ERR = 'DB. UPDATE CALL ERROR'
	CREATE_SUBSCR_TRANSACTION_ERR = 'CREATE SUBSCRIPTION TRANSACTION ERROR'
	CREATE_PROFILE_REQUEST_ERR = 'CREATE PROFILE REQUEST ERROR'
	GET_TRANSACT_ERR = 'GET SUBSCRIPTION TRANSACTION ERROR'

	# PBXDataService
	GET_AUDIO_ERR = 'GET AUDIO ERROR'
	GET_BALANCE_ERR = 'GET BALANCE ERROR'

	# CommonService
	WRITE_TEMP_FILE_ERR = 'WRITE TEMP FILE ERROR'
	CONVERT_TO_MP3_ERR = 'CONVERT TO MP3 ERROR'
	EMAIL_SEND_ERR = 'EMAIL SEND ERROR'

	# Disk Service
	CREATE_FOLDER_ERR = 'DISK. CREATE FOLDER ERROR'
	GET_UPLOAD_LINK_ERR = 'DISK. GET UPLOAD LINK ERROR'
	UPLOAD_FILE_ERR = 'DISK. FILE UPLOAD ERROR'
	GET_DOWNLOAD_LINK_ERR = 'DISK. GET DOWNLOAD LINK ERROR'
	DOWNLOAD_FILE_ERR = 'DISK. FOWNLOAD FILE ERROR'

	# controllers
	GET_CALL_RECORD_ERR = 'CONTROLLER. GET CALL RECORD ERROR'

	# Payment Service
	PAY_ERR = 'PAYMENT ERROR'

	# TransactAction
	TRANSACT_EXE_ERR = 'TRANSACT EXECUTION ERROR'

	INVLOG = 'INVLOG Invalid logging data'

	PCRERR = 'PCRERR Profile creation error'
	GTKERR = 'GTKERR Get token error'
	MCRERR = 'MCRERR Mail creation error'

	PMDERR = 'PMDERR Permission denied'

	UCLEXE = 'UCLEXE Update calls list executed succeed'
	UCLNTU = 'UCLNTU Nothing to update'
	UCLSWE = 'UCLSWE Succeed with errors'
	UCLUNS = 'UCLUNS Unsucceed'

	ECRERR = 'ECRERR Entity creation error'

	SAVE_ENTITY_ERR = 'SAVE ENTITY ERROR'


class LogService():
	def __init__(self):
		self.__logger = logging.getLogger('app_logger')
		self.__template = '[{callee}] {code}\n{data}'

	def __get_log_text(self, code, callee, data):
		return self.__template.format(callee=callee, code=code, data=self.__format_data(data))

	def error(self, code, **data):
		self.__logger.error(self.__get_log_text(code, inspect.stack()[1][3], data))

	def warning(self, code, **data):
		self.__logger.warning(self.__get_log_text(code, inspect.stack()[1][3], data))

	def info(self, code, **data):
		self.__logger.info(self.__get_log_text(code, inspect.stack()[1][3], data))

	def __format_data(self, data, iteration=0):
		template = '{space}{key}: {value}\n'
		formatted_data = ''
		if isinstance(data, dict):
			formatted_data += '\n' if iteration > 0 else ''
			for key, value in data.items():
				formatted_data += template.format(key=key, space=''.join(['  ' * iteration]), value=self.__format_data(value, iteration + 1))
		elif type(data) is str or type(data) is int or type(data) is bool:
			return data
		elif type(data) is unicode:
			return data.encode()
		elif isinstance(data, list) or type(data) is tuple:
			for d in data:
				formatted_data += self.__format_data(d, iteration + 1)
		elif isinstance(data, Code):
			return data.value
		return formatted_data