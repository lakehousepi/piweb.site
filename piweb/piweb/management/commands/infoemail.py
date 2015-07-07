from django.core.management.base import NoArgsCommand
from utils.scripts.infoemail import infoemail_html_with_image

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        infoemail_html_with_image()
