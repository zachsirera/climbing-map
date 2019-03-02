# This is a script to collect data to be used in the heat map.

# Import necessary libraries
import csv
import requests
import json

def main():
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

			data = response.json()
			routes = data['routes']

			print(len(routes))


if __name__ == "__main__":
	main()



