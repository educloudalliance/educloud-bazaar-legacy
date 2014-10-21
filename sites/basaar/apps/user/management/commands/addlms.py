from django.core.management.base import BaseCommand, CommandError
from oscar.core.loading import get_class, get_model
from django.template.defaultfilters import slugify


User = get_model('user', 'User')
Partner = get_model('partner', 'Partner')
Node = get_model('api', 'APINode')

class Command(BaseCommand):
    args = '<username  ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for u in args:
            username = u

        username = slugify(username)
        email = username + "@educloudalliance.org"

        # Check if there's username, email, partner or accesspoint by the same name
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists() or Partner.objects.filter(users=username).exists() or Node.objects.filter(uniquePath=username).exists():
            self.stdout.write('Partner already exists')
