# This is a script to collect data to be used in the heat map.

# Import necessary libraries
import csv
import requests
import json
import plotly.plotly
import pandas 

from math import floor
from statistics import median

# import states.json

states_list = []


def api_call():
	with open("coords.csv", "r") as csvfile:
		reader = csv.reader(csvfile, delimiter=',')

		# skip the first row, which is a header
		next(reader)

		# iterate across the document
		# the coords.csv has over 30,000 zip codes and their coordinates
		for row in reader:

			lat = row[1]
			lon = row[2]

			# Parameters for Mountain Project API
			url = "https://www.mountainproject.com/data/get-routes-for-lat-lon"
			parameters = {"lat": lat, "lon": lon, "maxDistance": "10", "minDiff": "5.6", "maxDiff": "5.16", "key": '110497345-b885de79bcbc861f3d5b9cf49c0e46e1'}

			response = requests.get(url, parameters)

			# Ensure that request was successful
			if response.status_code != 200:
				print('error')
				break

			data = response.json()
			routes = data['routes']

			print(len(routes))

def generate_colors():
	with open("states.json") as f:
		data = json.load(f)

		# Initialize route list for max and median later
		route_list = []

		states = data['states']

		# Find the largest number of routes in the states object
		for state in states:
			routes = int(state['routes'])

			route_list.append(routes)
			
		max_routes = max(route_list)

			
		# Generate rgb triples for each state
		for state in states:
			routes = int(state['routes'])
			ratio = routes / max_routes

			# colors are chosen based on a monochromatic scale for the webpage theme:

			# 		     r.   g.   b. 
			# darkest  = 24,  5,   0
			# middle   = 255, 54,  0
			# lightest = 255, 235, 229

			if ratio >= 0.5:
				r = floor(255 - ((255 - 24) / (1 - 0.5)) * (ratio - 0.5))
				g = floor(54 - ((54 - 5) / (1 - 0.5)) * (ratio - 0.5))
				b = 0
			else:
				r = 255
				g = floor(235 - ((235 - 54) / (1 - 0.5)) * ratio)
				b = floor(229 - ((229 - 0) / (1 - 0.5)) * ratio)
				

			state_rgb = (r, g, b)

			# Convert to hex
			state_hex = '#%02x%02x%02x' % state_rgb 

			print(state['state'], state_hex)

def test():
	with open('mapdata.js', 'r') as file:
		print("opened")
		line = file.readline()
		while line:
			print(line)
			line = file.readline()
		else: 
			print("no line")

if __name__ == "__main__":
	generate_colors()
	# test()



