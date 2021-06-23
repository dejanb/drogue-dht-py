#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys

import Adafruit_DHT
import time

import os
import json
import requests
from urlparse import urljoin
from urllib import urlencode, quote, quote_plus


# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    sys.exit(1)

data_schema = os.getenv('DATA_SCHEMA', "urn:drogue:iot:temperature")

geolocation = os.getenv('GEOLOCATION')
print(geolocation)
if geolocation is not None:
    geolocation = json.loads(geolocation)

endpoint = os.getenv('ENDPOINT', "https://http.sandbox.drogue.cloud")
print(endpoint)

app_id = os.getenv('APP_ID')
device_id = quote(os.environ['DEVICE_ID'])
device_password = os.getenv('DEVICE_PASSWORD')

denc = quote_plus(device_id)
auth = "%s@%s" % (denc, app_id)
#auth = "device@app"
print(auth)

path = "/v1/status"
url = urljoin(endpoint, path)

print(url)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        temp = "%.2f" % temperature
        hum = "%.2f" % humidity
        print('Temp=%s  Humidity=%s' % (temp, hum))
        status = {
            "temp": temp,
            "hum": hum,
            "geoloc": geolocation,
        }
        params = {
            "data_schema": data_schema
        }
        res = requests.post(url,
                            json=status,
                            auth=(auth, device_password),
                            headers={"Content-Type": "application/json"},
                            params=params
                            )
        print("Result: %s" % res)

    else:
        print('Failed to get reading. Try again!')
    time.sleep(30.0)

