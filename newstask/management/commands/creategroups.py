from django.contrib.auth.models import Group
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        author, created = Group.objects.get_or_create(name='author')
        subscriber, created = Group.objects.get_or_create(name='subscriber')
        author.save()
        subscriber.save()