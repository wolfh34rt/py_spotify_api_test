from spotifyapi import SpotifyAPI
from http.server import HTTPServer, BaseHTTPRequestHandler
from os import curdir, sep
from io import BytesIO

def main():
	try:
		spotify_current_context = SpotifyAPI("")
		httpd = HTTPServer(("localhost", 8090), HTTPRequestHandler)
		print("Running Server")
		httpd.serve_forever()
	except KeyboardInterrupt:
		print("INT received, shutting down the web server")
		httpd.socket.close()

class HTTPRequestHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		try:
			if self.path == "/":
				self.path="/index.html"
			elif self.path == "/gettoken":
				self.path="/index.html"
			else:
				raise IOError

			send_reply = False
			
			if self.path.endswith(".html"):
				mime_type="text/html"
				send_reply = True
			elif self.path.endswith(".jpg"):
				mime_type="image/jpg"
				send_reply = True
			elif self.path.endswith(".gif"):
				mime_type="image/gif"
				send_reply = True
			elif self.path.endswith(".js"):
				mime_type="application/javascript"
				send_reply = True
			elif self.path.endswith(".css"):
				mime_type="text/css"
				send_reply = True

			if send_reply == True:
				file = open(curdir + sep + self.path, "rb") 
				self.send_response(200)
				self.send_header("Content-type",mime_type)
				self.end_headers()
				self.wfile.write(file.read())
				file.close()
			return
			
		except IOError:
			self.send_error(404,"File Not Found: %s" % self.path)


	def do_POST(self):
		content_length = int(self.headers["Content-Length"])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = BytesIO()
		response.write(b"This is POST request. ")
		response.write(b"Received: ")
		response.write(body)
		self.wfile.write(response.getvalue())
		
if __name__ == "__main__" : main()