from django.core.management.base import NoArgsCommand
from utils.scripts.infoemail import infoemail_html

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        infoemail_html()
