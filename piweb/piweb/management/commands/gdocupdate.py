from django.core.management.base import NoArgsCommand
from utils.scripts.gdocupdate import gdocupdate

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        gdocupdate()
