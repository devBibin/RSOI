import matplotlib
matplotlib.use('Agg')
from scipy.interpolate import spline
from matplotlib import pyplot as plt
from matplotlib import cm
import datetime

import numpy as np
import os


def create_activity_dinamics(data):
	arr = data["distribution"]

	x = []
	y = []
	i = 0
	for el in arr:
		x.append(i)
		y.append(el[str(i)])
		i = i + 1

	plt.plot(x, y, color="r")
	plt.title("Monitoring period \n" + data["period"])
	plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off
	
	plt.savefig("renderapp/static/renderapp/dist_chart.jpg",
		dpi=199, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)
	plt.close()

def create_auth_percantage_chart(tries, completed):
	labels = 'Completed', ''
	c_percentage = 1. * completed/tries * 100
	sizes = [c_percentage, 100 - c_percentage]

	fig1, ax1 = plt.subplots()
	ax1.set_color_cycle(['y', 'b'])
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	plt.title("Authorization statistics")

	plt.savefig("renderapp/static/renderapp/auth_chart.jpg",
		dpi=199, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)
	plt.close()


# Followers and followed bar chart
def create_uri_chart(data):
	uri_array =  data["uri_array"]
	x = []
	uri_lst = []
	data = []
	i = 0
	for el in uri_array:
		if (len(el["uri"]) > 40):
			el["uri"] = el["uri"][:40] + "..."
		uri_lst.append(el["uri"])
		data.append(el["total"])
		x.append(i)
		i = i + 1

	print uri_lst
	fig, ax = plt.subplots()

	plt.bar(x, data, color="blue")
	
	for i in range(len(x)):
		plt.annotate(uri_lst[i], xy=(x[i]-0.3,max(data)), textcoords='data', rotation = "vertical")
	
	plt.title("Distribution in calls by API methods")

	plt.savefig("renderapp/static/renderapp/uri_chart.jpg",
		dpi=199, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)
	plt.close()