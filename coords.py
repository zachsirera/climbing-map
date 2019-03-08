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

		with open("hold.txt", "w") as h:	
			
			for state in states:
				routes = int(state['routes'])

				if routes == 0:
					state_hex = "default"
				else:
					# Generate rgb triples for each state
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

				# Need to configure print to this format:
				# AL: {
				# 	name: "Alabama",
				# 	description: "Routes: 1290",
				# 	color: "#ffdad0",
				# 	hover_color: "default",
				# 	url: "https://www.mountainproject.com/area/105905173/alabama"
				# },

				h.write(f"{state['state']}: ")
				h.write("{ \n")
				h.write(f"\t\tname: '{state['name']}'")
				h.write(", \n")
				if routes == 0:
					h.write("\t\tdescription: 'Climbing Wasteland'")
					h.write(", \n")
				else:
					h.write(f"\t\tdescription: '{routes} routes'")
					h.write(", \n")		
				h.write(f"\t\tcolor: '{state_hex}'")
				h.write(", \n")
				h.write(f"\t\thover_color: 'default', \n")		
				h.write(f"\t\turl: '{state['url']}' \n")
				h.write("\t}, \n")
			

				
			

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



