from django.core.management.base import NoArgsCommand
from utils.scripts.info import info

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		info()