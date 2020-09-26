#!/usr/bin/python

import time
import pigpio
import DHT22


# initialize library to do the low-level data reading
pi = pigpio.pi()


# Intervals of about 2 seconds or less will eventually hang the DHT22
# one per minute is totally fine for current use case
QUERY_INTERVAL = 60


# initialize sensors
sensor_outside = DHT22.sensor(pi, 2)
sensor_drivers_cabin = DHT22.sensor(pi, 3)
sensor_over_table = DHT22.sensor(pi, 4)
sensor_over_bed = DHT22.sensor(pi, 5)
sensor_temperature_sensor = DHT22.sensor(pi, 6)
sensor_ventilator = DHT22.sensor(pi, 7)

sensors = [("Outside", sensor_outside), ("Driver's cabin", sensor_drivers_cabin), ("Over the table", sensor_over_table), ("Over the bed", sensor_over_bed), ("At the temperature sensor", sensor_temperature_sensor), ("Close to a ventilator", sensor_ventilator)]

reading_counter = 0

next_reading = time.time()

while True:

  reading_counter += 1
  current_time = time.time()
  time_string = time.strftime("%Y%m%d %H:%M:%S", time.gmtime())

  for sensordata in sensors:
      name = sensordata[0]
      sensor = sensordata[1]
      
      # read data from sensor, wait a bit....
      sensor.trigger()
      time.sleep(0.2)
      
      # output: date, sensor, temperature
      print("{} {} {}".format(time_string, name, sensor.temperature()))

  next_reading += QUERY_INTERVAL

  time.sleep(next_reading-time.time())  # Overall INTERVAL second polling.


for sensordata in sensors:

  sensordata[1].cancel()

pi.stop()




