import json
import time

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
	
	tr = TempReader(temp_sensor_pin=pins.TEMP_SENSOR)
	datadict.update(tr.read_temp())
	
	datadict.update(both_ip())
	
	
	datastring = json.dumps(datadict)
	es = EmailSender(servername=gdocs.SERVERNAME, username=gdocs.USERNAME,
			password=gdocs.PASSWORD)
	es.sendmail(fromaddr=gdocs.USERNAME, toaddrs=['jbrodie@gmail.com'],
			subject='Temperature update', body=datastring)
	
	green.off()