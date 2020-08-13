from urllib.request import Request, urlopen
from io import BytesIO
import base64
import math
import colorsys

class Helpers:
	def CheckValidFileTypeInPath(path):
		send_reply = False
		mime_type = ""

		"""if path.endswith(".html"):
			mime_type="text/html"
			send_reply = True"""
		if path.endswith(".jpg"):
			mime_type="image/jpg"
			send_reply = True
		elif path.endswith(".gif"):
			mime_type="image/gif"
			send_reply = True
		elif path.endswith(".js"):
			mime_type="application/javascript"
			send_reply = True
		elif path.endswith(".css"):
			mime_type="text/css"
			send_reply = True

		return send_reply,mime_type

	def GetURLByteContent(url):
		contents = urlopen(Request(url)).read()
		return contents

	def SortColours (line, repetitions=1):
		r,g,b = tuple(line["album"]["dominant_colour"].split("|"))
		print("red: {} green: {} blue: {}".format(r,g,b))
		lum = math.sqrt( .241 * float(r) + .691 * float(g) + .068 * float(b) )

		h, s, v = colorsys.rgb_to_hsv(float(r),float(g),float(b))

		h2 = int(h * repetitions)
		lum2 = int(lum * repetitions)
		v2 = int(v * repetitions)

		return (h2, lum, v2)