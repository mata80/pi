"""
Python sample for Raspberry Pi which reads temperature and humidity values from
a DHT22 sensor, and sends that data to Power BI for use in a streaming dataset.
"""

import urllib, urllib2, time
from datetime import datetime
import Adafruit_DHT as dht
import random

# type of sensor that we're using
SENSOR = dht.DHT22 	

# pin which reads the temperature and humidity from sensor
PIN = 4			

# REST API endpoint, given to you when you create an API streaming dataset
# Will be of the format: https://api.powerbi.com/beta/<tenant id>/datasets/< dataset id>/rows?key=<key id>
REST_API_URL = "https://api.powerbi.com/beta/a9e228d8-83e3-45e1-815b-6119aeec4a72/datasets/46dfe4e4-6dc3-43a6-a75b-3ff7c375f8d2/rows?key=k5kL%2BKXmeL1XUhvzVCdnaeMkhMxCn9KnV5IUMyLmIhTDxxrNl07IDlRg8sTWr8ssA8oDlMF4Yqii%2Fo17Aqi92g%3D%3D"



# Gather temperature and sensor data and push to Power BI REST API
while True:
	try:
		# read and print out humidity and temperature from sensor
		#humidity,temp = dht.read_retry(SENSOR, PIN)
		humidity = 0
		temp = random.randint(1,30)

		print 'Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temp, humidity)
		
		# ensure that timestamp string is formatted properly
		now = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%Z")
	
		# data that we're sending to Power BI REST API
		data = '[{{ "timestamp": "{0}", "temperature": "{1:0.1f}", "humidity": "{2:0.1f}" }}]'.format(now, temp, humidity)
	
		# make HTTP POST request to Power BI REST API
		req = urllib2.Request(REST_API_URL, data)
		response = urllib2.urlopen(req)
		print("POST request to Power BI with data:{0}".format(data))
		print("Response: HTTP {0} {1}\n".format(response.getcode(), response.read()))	
	
		time.sleep(1)
	except urllib2.HTTPError as e:
		print("HTTP Error: {0} - {1}".format(e.code, e.reason))
	except urllib2.URLError as e:
		print("URL Error: {0}".format(e.reason))
	except Exception as e:
		print("General Exception: {0}".format(e))
