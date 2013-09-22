import json
import datetime

from utils.ip import both_ip
from utils.led import LEDController
from utils.temperature import TempReader

from utils.config import pins

from piweb.models import IPReading, IPSeries, TempReading, TempSeries

def gatherdata():
	green = LEDController(led_pin=pins.GREEN_LED)
	green.on()
	
	# Get IP data, snap timestamp, insert data
	ipaddrs = both_ip()
	timestamp = datetime.datetime.now()	
	
	global_ips = IPSeries.objects.get(name='Global')
	local_ips = IPSeries.objects.get(name='Local')
	
	global_ipr = IPReading(
		ipseries=global_ips,
		value=ipaddrs['global_ip'],
		timestamp=timestamp
	)
	global_ipr.save()
	
	local_ipr = IPReading(
		ipseries=local_ips,
		value=ipaddrs['local_ip'],
		timestamp=timestamp
	)
	local_ipr.save()
	
	# Get temp data, snap timestamp, insert data
	tr = TempReader(temp_sensor_pin=pins.TEMP_SENSOR)
	temp = tr.read_temp()
	timestamp = datetime.datetime.now()
	
	upstairs_ts = TempSeries.objects.get(name='Upstairs')
	upstairs_tr = TempReading(
		tempseries=upstairs_ts,
		value=temp['temp_f'],
		scale='F',
		timestamp=timestamp
	)
	upstairs_tr.save()
	
	green.off()