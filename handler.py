from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
from utils import Helpers
from io import BytesIO
from spotifyapi import SpotifyAPI
import urllib
import json
import requests
import appglobals
import os.path

class DefaultRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			#spotifyapi = SpotifyAPI(self.server.server_name)
			send_reply = ""
			mime_type = ""

			# add path methods/functions and separate them into different files.
			if self.path == "/":
				#need to fix this later to handle html files seperately.
				self.path="/pages/index.html"
				send_reply = True
				mime_type = "text/html"
			elif self.path == "/gettoken":
				mime_type == "text/plain"
				send_reply == True
			elif "/auth_token_return" in self.path :
				spotifyapi = SpotifyAPI(appglobals.Vars.GetDebugHost())
				spotifyapi.SaveAuthCode(self.path)
				self.path="/pages/got_token.html"
				send_reply,mime_type = Helpers.CheckValidFileTypeInPath(self.path)
			elif self.path == "/rainbow_sort_album_data" :
				self.path = "/pages/rainbow_sort_album_data.html"
				send_reply = True
				mime_type = "text/html"
			elif self.path == "/test_api" :
				spotifyapi = SpotifyAPI(appglobals.Vars.GetDebugHost())
				print(spotifyapi.GetSpotifyUserLibraryAlbums())
			elif "/js/" in self.path :
				send_reply,mime_type = Helpers.CheckValidFileTypeInPath(self.path)
				self.path = self.path.replace("/js/","/dist/js/")
			elif "/img/" in self.path :
				send_reply,mime_type = Helpers.CheckValidFileTypeInPath(self.path)
			elif "/css/" in self.path :
				send_reply,mime_type = Helpers.CheckValidFileTypeInPath(self.path)
			else:
				raise IOError

			# add reply methods/functions
			if send_reply == True:
				file = open(curdir + sep + self.path, "rb") 
				self.send_response(200)
				self.send_header("Content-Type",mime_type)
				self.end_headers()
				self.wfile.write(file.read())
				file.close()
			return
			
		except IOError:
			self.send_error(404,"File Not Found: %s" % self.path)


	def do_POST(self):
		send_reply = ""
		mime_type = ""
		response_json = ""
		#spotifyapi = SpotifyAPI(self.server.server_name)

		# add path methods/functions and separate them into different files.
		if self.path == "/get_authorize_app_uri":
			send_reply = True
			spotifyapi = SpotifyAPI(appglobals.Vars.GetDebugHost())
			response_json = { "authorize_uri" : spotifyapi.GetAuthorizeAppURI() }
			mime_type = "application/json"
		elif self.path == "/get_saved_albums":
			send_reply = True
			spotifyapi = SpotifyAPI(appglobals.Vars.GetDebugHost())
			response_json = { "data" : spotifyapi.GetSpotifyUserLibraryAlbums() }
			mime_type = "application/json"
			send_reply = True

		if send_reply:
			# test post data
			#content_length = int(self.headers["Content-Length"])
			#json_data = json.loads(self.rfile.read(content_length).decode("utf-8"))
			#print(json_data)
			self.send_response(200)
			self.send_header("Content-Type", mime_type)
			self.end_headers()
			response = BytesIO()
			response.write(json.dumps(response_json).encode("utf-8"))
			self.wfile.write(response.getvalue())

		return