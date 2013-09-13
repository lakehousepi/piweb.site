from django.core.management.base import NoArgsCommand

from piweb.utils.email import EmailSender
from piweb.utils.gspreadsheet import GSpreadsheetUpdater
from piweb.utils.ip import global_ip_from_jsonip, local_ip
from piweb.utils.led import LEDController
from piweb.utils.temperature import TempReader

from piweb.utils.config import gdocs, pins

class Command(NoArgsCommand):
	def handle_noargs(self):
		