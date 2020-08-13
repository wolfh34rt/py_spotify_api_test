from io import BytesIO
from config import spotify
from os import curdir, sep
from colour_sort_lib import ColourSorting
from utils import Helpers
import os.path
import json
import requests
import urllib
import appglobals
import base64
import numpy

class SpotifyAPI():
	def __init__(self,server_name):
		self.__authorize_uri = "https://accounts.spotify.com/authorize"
		self.__token_uri = "https://accounts.spotify.com/api/token"
		self.__authorization_scopes = "user-library-read playlist-read-private playlist-read-collaborative user-read-email user-read-private"
		self.__spotify_user_data_uri = "https://api.spotify.com/v1/me"
		self.__spotify_user_library_albums = "https://api.spotify.com/v1/me/albums"
		self.__server_name = server_name
		self.__token = ""

		is_auth_successful = False
		
		with open("./secrets.json","r") as file:
			config_objects = json.load(file)

			self.__default_config = spotify.Config(
				config_objects["db_user"],
				config_objects["db_pw"],
				config_objects["spotify_client_id"],
				config_objects["spotify_cleint_secret"]
			)

			file.close()

		if os.path.isfile("test_auth_token.json"):
			self._authorize_app()

			if os.path.isfile("test_access_token.json"):
				with open("test_access_token.json","r") as file:
					json_data = json.load(file)

					if "access_token" in json_data:
						self.__token = json_data["access_token"]
					else:
						self.__token = "error"

					file.close()
		else:
			self.__token = "error"

	def _set_token(self,token):
		self.__token = token

	def _get_token(self):
		return self.__token

	def _refresh_token(self):
		is_auth_successful = False
		refresh_token = ""
		response = None
		refresh_token_data = None

		with open("./test_access_token.json","r") as file:
			refresh_token_data = json.load(file)

			if "refresh_token" in refresh_token_data:
				refresh_token = refresh_token_data["refresh_token"]
			else:
				refresh_token = "error"

			file.close()

		if refresh_token != "error":
			encoded_app_data = base64.urlsafe_b64encode((self.GetDefaultConfig().GetClientID() + ":" + self.GetDefaultConfig().GetClientSecret()).encode("utf-8")).decode("utf-8")

			post_header = { 
				"Content-Type" : "application/x-www-form-urlencoded", 
				"Authorization" : "Basic {}".format(encoded_app_data)
			}

			post_body = {  
				"grant_type" : "refresh_token",
				"refresh_token" : refresh_token,
				"redirect_uri" : "http://{}/auth_token_return".format(self.__server_name)
			}

			response = requests.post(self.GetTokenURI(), data = post_body, headers = post_header)

			if response.status_code == 200:
				is_auth_successful = True
			else:
				is_auth_successful = False

			if is_auth_successful:
				try:
					json_data = json.loads(response.text)

					if "access_token" in json_data:
						self.__token = json_data["access_token"]
						refresh_token_data["access_token"] = json_data["access_token"]

						if "refresh_token" in json_data:
							refresh_token_data["refresh_token"] = json_data["refresh_token"]
					else:
						self.__token = "error"

					with open("test_access_token.json", "w") as access_token_file:
						access_token_file.write(json.dumps(refresh_token_data))
						access_token_file.close()
				except Exception as e:
					print(e)
					is_auth_successful = False

		return is_auth_successful

	def _authorize_app(self):
		is_auth_successful = False
		response = None

		if os.path.isfile("test_access_token.json"):
			is_auth_successful = self._refresh_token()
		else:
			print("opening auth token file")
			with open("./test_auth_token.json","r") as file:
				json_data = json.load(file)
				auth_code = json_data["auth_code"][0]
				file.close()

			encoded_app_data = base64.urlsafe_b64encode((self.GetDefaultConfig().GetClientID() + ":" + self.GetDefaultConfig().GetClientSecret()).encode("utf-8")).decode("utf-8")

			post_header = { 
				"Content-Type" : "application/x-www-form-urlencoded", 
				"Authorization" : "Basic {}".format(encoded_app_data)
			}

			post_body = {  
				"grant_type" : "authorization_code",
				"code" : auth_code,
				"redirect_uri" : "http://{}/auth_token_return".format(self.__server_name)
			}

			response = requests.post(self.GetTokenURI(), data = post_body, headers = post_header)

			if response.status_code == 200:
				json_data = json.loads(response.text)

				if "access_token" in json_data:
					self.__token = json_data["access_token"]
				else:
					self.__token = "error"

				try:
					with open("test_access_token.json", "w") as access_token_file:
						access_token_file.write(response.text)
						access_token_file.close()
					
					is_auth_successful = True
				except Exception as e:
					print(e)
			else:
				self._set_token = "error"

		return is_auth_successful

	def GetSpotifyUserData(self):
		if self._get_token() != "error":
			get_header = {
				"Authorization" : "Bearer {}".format(self._get_token())
			}
			get_body = {}

			response = requests.get(self.GetSpotifyUserDataURI(), data = get_body, headers = get_header)
			
			return response.text
		else: 
			return json.dumps({"error": "error"})
			

	def GetSpotifyUserLibraryAlbums(self):
		if self._get_token() != "error":
			response = None
			album_data = ""
			get_header = {
				"Authorization" : "Bearer {}".format(self._get_token())
			}
			get_body = {}

			if os.path.isfile("album_data.json"):
				with open("album_data.json", "r") as album_data_file:
					album_data = album_data_file.read()
					album_data_file.close()
			else:
				response = requests.get(self.GetSpotifyUserLibraryAlbumsURI(), data = get_body, headers = get_header)

				if response.status_code == 200:
					album_data = response.text
				elif response.status_code == 401:
					if self._authorize_app():
						response = requests.get(self.GetSpotifyUserLibraryAlbumsURI(), data = get_body, headers = get_header)
						album_data = response.text
					else:
						album_data = json.dumps({"error": "could not authenticate."})
				else:
					album_data = json.dumps({"error": "could not authenticate."})
					print(response.status_code)
					print(response.text)
					print(self._get_token())

				# debug. remove at some point.
				if not os.path.isfile("album_data.json"):
					with open("album_data.json", "w") as album_data_file:
						print("writing file")
						album_data_file.write(json.dumps(json.loads(album_data), sort_keys=True, indent=4, separators=(',', ': ')))
						album_data_file.close()

			album_json = []
			colour_sorting = ColourSorting()

			for album_add in (json.loads(album_data))["items"]:
				for key in album_add.keys():
					if key == "album":
						r,g,b = colour_sorting.GetDominantColour(numpy.frombuffer(Helpers.GetURLByteContent(album_add[key]["images"][1]["url"]),numpy.uint8))
						album_json.append({
							"album":{
								"image_url" : album_add[key]["images"][1]["url"],\
								"artist_name": album_add[key]["artists"][0]["name"],\
								"artist_url": album_add[key]["artists"][0]["href"],\
								"album_name": album_add[key]["name"],\
								"dominant_colour": "{}|{}|{}".format(r,g,b)
							}
						})

			album_json.sort(key=lambda album: Helpers.SortColours(album,8))

			return json.dumps(album_json, sort_keys=True, indent=4, separators=(',',': '))
		else: 
			return json.dumps({"error": "could not retrieve a valid spotify access token."})


	def GetTokenURI(self):
		return self.__token_uri

	def GetSpotifyUserDataURI(self):
		return self.__spotify_user_data_uri

	def GetSpotifyUserLibraryAlbumsURI(self):
		return self.__spotify_user_library_albums

	def GetAuthorizationURI(self):
		return self.__authorize_uri

	def GetAuthorizeAppURI(self):
		return self.GetAuthorizationURI() + "?" + urllib.parse.urlencode({"client_id" : self.GetDefaultConfig().GetClientID(), "response_type" : "code", "scope" : self.GetAuthorizationScopes(), "redirect_uri" : "http://{}/auth_token_return".format(self.__server_name)})

	def GetDefaultConfig(self):
		return self.__default_config

	def GetAuthorizationScopes(self):
		return self.__authorization_scopes

	def SaveAuthCode(self,path):
		try:
			parsed_url = urllib.parse.urlparse(path)

			with open("test_auth_token.json", "w") as token_file:
				token_file.write(json.dumps({ "auth_code" : urllib.parse.parse_qs(parsed_url.query)["code"] }))
				token_file.close()
		except Exception as e:
			print(e)