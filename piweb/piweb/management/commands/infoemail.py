from django.core.management.base import NoArgsCommand
from utils.scripts.infoemail import infoemail

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        infoemail()