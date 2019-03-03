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
		avg_routes = max_routes / 2

			
		# Generate rgb triples for each state
		for state in states:
			routes = int(state['routes'])

			# colors are chosen based on a monochromatic scale for the webpage theme:

			# 		     r.   b.   g. 
			# darkest  = 24,  5,   0
			# median   = 255, 54,  0
			# lightest = 255, 235, 229

			if routes >= avg_routes:
				r = floor(255 - ((routes - avg_routes) / (max_routes - avg_routes)) * (255 - 24))
				b = floor(54 - ((routes - avg_routes) / (max_routes - avg_routes)) * (54 - 5))
				g = floor(0 + ((routes - avg_routes) / (max_routes - avg_routes)) * (229 - 0))
			else:
				r = 255 
				b = floor(235 - (routes / avg_routes) * (235 - 54))
				g = 0


			state_rgb = (r, g, b)

			# Convert to hex
			# state_hex = '#%02x%02x%02x' % state_rgb 

			print(state_rgb)



if __name__ == "__main__":
	generate_colors()



