import datetime

from utils.config import gdocs, pins

from utils.temperature import TempReader
from utils.ip import both_ip
from utils.led import LEDController
from utils.gspreadsheet import GSpreadsheetUpdater

def gdocupdate():
    green = LEDController(led_pin=pins.GREEN_LED)
    green.on()

    datadict = {}

    timestamp = datetime.datetime.now()
    datadict['date'] = timestamp.strftime('%m/%d/%Y')
    datadict['time'] = timestamp.strftime('%H:%M:%S')

    tr = TempReader(temp_sensor_pin=pins.TEMP_SENSOR)
    temp = tr.read_temp()
    datadict['tempcentigrade'] = str(temp['temp_c'])
    datadict['tempfahrenheit'] = str(temp['temp_f'])

    ipaddrs = both_ip()
    datadict['localip'] = ipaddrs['local_ip']
    datadict['globalip'] = ipaddrs['global_ip']

    gsu = GSpreadsheetUpdater(gdocs.USERNAME, gdocs.PASSWORD, None, gdocs.SPREADSHEETKEY, gdocs.WORKSHEETID)
    gsu.login()
    gsu.insertrow(datadict)
    
    green.off()
