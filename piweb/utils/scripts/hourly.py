import json

from utils.email import EmailSender
from utils.gspreadsheet import GSpreadsheetUpdater
from utils.ip import global_ip_from_jsonip, local_ip
from utils.led import LEDController
from utils.temperature import TempReader

from utils.config import gdocs, pins

def hourly():
	tr = TempReader(temp_sensor_pin=pins.TEMP_SENSOR)
	tempdict = tr.read_temp()
	tempstring = json.dumps(tempdict)
	
	es = EmailSender(servername=gdocs.SERVERNAME, username=gdocs.USERNAME,
			password=gdocs.PASSWORD)
	es.sendmail(fromaddr=gdocs.USERNAME, toaddrs=['jbrodie@gmail.com'],
			subject='Temperature update', body=tempstring)
			