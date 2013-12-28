#!/usr/bin/python

"""
A 2d mouse 
"""

import gramme
from pymouse import PyMouse
from logbook import Logger
from decimalfilter import DecimalFilter

log 			= Logger('apps: plotter', level=0)
mouse 			= PyMouse()
time_interval 	= 1/73 #set it to 1/f where f is frequency of stream
time_squared 	= time_interval**2

DF 				= DecimalFilter(0,0,precision=2)
amplification 	= 100

@gramme.server(3030, poll_interval=time_interval)
def mouse(data):
	global mouse, time_interval, DF
	try:
		data = data.split(',')[2:4] #x,y accelration
		[ax,ay] = DF.update( float(data[0]), float(data[1]) ).filtered()
		[sx, sy] = mouse.position()
		log.info("Encountered accelration (%s, %s)"%(ax,ay))
		if ax or ay:
			[sx2, sy2] = mouse.position()
			log.info("Mouse moved from (%s, %s) to (%s, %s)"%(sx,sy,sx2,sy2))
			mouse.move(sx+0.5*ax*amplification*time_squared, sy+0.5*ay*amplification*time_squared)
	except KeyboardInterrupt:
		raise #let gramme handle this