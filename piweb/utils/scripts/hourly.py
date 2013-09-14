import json
import datetime

from utils.email import EmailSender
from utils.gspreadsheet import GSpreadsheetUpdater
from utils.ip import both_ip
from utils.led import LEDController
from utils.temperature import TempReader

from utils.config import gdocs, pins

def hourly():
	green = LEDController(led_pin=pins.GREEN_LED)
	green.on()
	
	datadict = {}
	
	timestamp = datetime.datetime.now()
	datadict['date'] = timestamp.strftime('%m/%d/%Y')
	datadict['time'] = timestamp.strftime('%H:%M:%S')

	tr = TempReader(temp_sensor_pin=pins.TEMP_SENSOR)
	temp = tr.read_temp()
	datadict['tempcentigrade'] = str(temp['temp_c'])
	datadict['tempfarenheit'] = str(temp['temp_f'])
	
	ipaddrs = both_ip()
	datadict['localip'] = ipaddrs['local_ip']
	datadict['globalip'] = ipaddrs['global_ip']
	
	datastring = json.dumps(datadict)
	
	es = EmailSender(servername=gdocs.SERVERNAME, username=gdocs.USERNAME,
			password=gdocs.PASSWORD)
	es.sendmail(fromaddr=gdocs.USERNAME, toaddrs=['jbrodie@gmail.com'],
			subject='Temperature update', body=datastring)
	
	green.off()