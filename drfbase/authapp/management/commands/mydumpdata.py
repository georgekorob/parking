from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        for name in ['authapp', 'camsapp']:
            with open(f'./{name}/fixtures/{name}.json', 'w') as file:
                call_command('dumpdata', name, format='json', indent=3, stdout=file)
