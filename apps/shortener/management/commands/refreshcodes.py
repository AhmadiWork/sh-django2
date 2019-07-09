from django.core.management.base import BaseCommand

from apps.shortener.models import AlmaURL


class Command(BaseCommand):
    help = 'Refrehes all AlmaURL shortcodes'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)

    def handle(self, *args, **options):
        return AlmaURL.objects.refresh_shortcodes(items=options['items'])
