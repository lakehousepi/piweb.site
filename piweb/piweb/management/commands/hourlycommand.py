from django.core.management.base import NoArgsCommand
from utils.scripts.hourly import hourly

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		hourly()