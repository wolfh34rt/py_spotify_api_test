class Config():
	def __init__(self,db_user,db_pw,spotify_client_id,spotify_client_secret):
		self.__db_user = db_user
		self.__db_pw = db_pw
		self.__spotify_client_id = spotify_client_id
		self.__spotify_client_secret = spotify_client_secret

	def GetDbUser(self):
		return self.__db_user

	def GetDbPw(self):
		return self.__db_pw

	def GetClientID(self):
		return self.__spotify_client_id

	def GetClientSecret(self):
		return self.__spotify_client_secret