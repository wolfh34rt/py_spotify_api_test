from PIL import Image
from matplotlib import pyplot
from matplotlib import cm
from utils import Helpers
from sklearn.cluster import KMeans
import json
import cv2
import numpy

''' 
TODO: Move to unit test.
def main():
	image = numpy.frombuffer(Helpers.GetURLByteContent("https://www.color-hex.com/palettes/23160.png"),numpy.uint8)
	colour_sorting = ColourSorting()
	r,g,b = colour_sorting.GetDominantColour(image)
	print("r: {} g: {} b: {}".format(r,g,b))
'''

class ColourSorting():
	def __init__(self):
		pass

	def _get_histogram(self, cluster):
		bins = numpy.arange(0, len(numpy.unique(cluster.labels_)) + 1)
		(histogram, _) = numpy.histogram(cluster.labels_, bins=bins)

		histogram = histogram.astype("float")
		histogram /= histogram.sum()

		return histogram
		
	def _plot_colours_2d(self, histogram, centroids):
		bar = numpy.zeros((50, 300, 3), dtype="uint8")
		start_x_point = 0

		for (percent, colour) in zip(histogram, centroids):
			end_x_point = start_x_point + (percent * 300)
			cv2.rectangle(bar, (int(start_x_point), 0), (int(end_x_point), 50),
						  colour.astype("uint8").tolist(), -1)
			start_x_point = end_x_point

		return bar


	def GetDominantColour(self, image_data):
		# use ' nparr = numpy.frombuffer(<byte buffer>, numpy.uint8) ' to generate data
		image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = image.reshape((image.shape[0] * image.shape[1],3))
		cluster = KMeans(n_clusters=3)
		cluster.fit(image)

		histogram = self._get_histogram(cluster)
		bar_graph = self._plot_colours_2d(histogram, cluster.cluster_centers_)

		''' for checking clusters
		pyplot.imshow(bar_graph)
		pyplot.show()
		'''

		bar_graph_image = Image.fromarray(bar_graph)
		image_width, image_height = bar_graph_image.size
		current_rgb_values = ""
		current_colours_count = 0
		colour_count_array = []

		for i in range(0,image_width,1):
			r,g,b = bar_graph_image.getpixel((i,0))

			if("{}|{}|{}".format(r,g,b) != current_rgb_values):
				if len(colour_count_array) == 0 and i == 0:
					current_rgb_values = "{}|{}|{}".format(r,g,b)
					current_colours_count += 1
				else:
					colour_count_array.append({current_rgb_values : current_colours_count})
					current_rgb_values = "{}|{}|{}".format(r,g,b)
					current_colours_count = 0
			else:
				if not i == image_width-1:
					current_colours_count += 1
				else:
					current_colours_count += 1
					colour_count_array.append({current_rgb_values : current_colours_count})

		return tuple(max(colour_count_array[0],key=lambda item:item[1]).split("|"))