from django.core.management.base import NoArgsCommand
from utils.scripts.makegraphs import makegraphs

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        makegraphs()
