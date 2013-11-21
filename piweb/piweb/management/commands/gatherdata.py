from django.core.management.base import NoArgsCommand
from utils.scripts.gatherdata import gatherdata

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        gatherdata()