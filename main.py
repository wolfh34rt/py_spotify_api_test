from spotifyapi import SpotifyAPI
from http.server import HTTPServer, BaseHTTPRequestHandler
from webserver import WebServer
from os import curdir, sep
from io import BytesIO
import handler
import ssl

def main():
	default_handler = handler.DefaultRequestHandler
	httpd_context = WebServer.CreateWebServerContext("razorwolf.sixwolfmedia.local",8090,default_handler)
	httpd_context.socket = ssl.wrap_socket(httpd_context.socket, certfile='./test.pem', server_side=True)

	try:
		print("Starting HTTP Server")
		httpd_context.serve_forever()
	except IOError as e:
		print(e)
	except KeyboardInterrupt as e:
		print(e)
	finally:
		print()
		print("Killing Webserver")
		httpd_context.shutdown()
		
if __name__ == "__main__" : main()