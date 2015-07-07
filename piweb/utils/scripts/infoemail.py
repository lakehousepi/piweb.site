import json
import datetime

from django.template import Context, loader

from utils.emailer import EmailSender
from utils.gspreadsheet import GSpreadsheetUpdater
from utils.ip import both_ip
from utils.led import LEDController
from utils.temperature import TempReader

from utils.config import gdocs, pins

from django.contrib.auth.models import Group, User

def infoemail():
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

    datastring = json.dumps(datadict, indent=4)

    infogroup = Group.objects.get(name='Daily Email')
    infousers = infogroup.user_set.all()

    infoemaillist = []
    for u in infousers:
        infoemaillist.append(u.email)

    es = EmailSender(servername=gdocs.SERVERNAME, username=gdocs.USERNAME,
            password=gdocs.PASSWORD)
    es.sendmail(fromaddr=gdocs.USERNAME, toaddrs=infoemaillist,
            subject='Temperature update', body=datastring)

    green.off()

def infoemail_html():
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

    datastring = json.dumps(datadict, indent=4)

    infogroup = Group.objects.get(name='Daily Email')
    infousers = infogroup.user_set.all()

    infoemaillist = []
    for u in infousers:
        infoemaillist.append(u.email)

    t = loader.get_template('utils/email.html')
    c = Context({'dd': datadict})
    h = t.render(c)

    es = EmailSender(servername=gdocs.SERVERNAME, username=gdocs.USERNAME,
            password=gdocs.PASSWORD)
    es.sendmail_html(fromaddr=gdocs.USERNAME, toaddrs=infoemaillist,
            subject='Temperature update (html)', textbody=datastring,
            htmlbody=h)

    green.off()
