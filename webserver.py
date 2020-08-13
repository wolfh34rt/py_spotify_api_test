from http.server import HTTPServer, BaseHTTPRequestHandler

class WebServer:
	def CreateWebServerContext(address,port,handler):
		try:
			httpd_context = HTTPServer((address, port), handler)
			print("Web server created.")
			return httpd_context
		except:
			print("Could not create web server context")