from django.core.management.base import BaseCommand, CommandError
from oscar.core.loading import get_class, get_model
from django.template.defaultfilters import slugify
from rest_framework.authtoken.models import Token


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

        # Check if username has been taken
        if User.objects.filter(username=username).exists():
            self.stdout.write('User %s already exists' % username)
            return 0

        # Check if email has been taken
        if User.objects.filter(email=email).exists():
            self.stdout.write('Email %s already exists' % email)
            return 0

        # Check if there's already a partner with that name

        if Partner.objects.filter(name=username).exists():
            self.stdout.write('Partner %s already exists' % username)
            return 0

        if Node.objects.filter(uniquePath=username).exists():
            self.stdout.write('Root node %s/ already exists' % username)
            return 0

        # If everything is okay, create password
        password = User.objects.make_random_password()

        # Create a user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create new partner
        newPartner = Partner(name=username)
        newPartner.save()
        # ... and link it to the new user
        newPartner.users.add(user)

        # Create root node
        rootNode = Node(uniquePath=username, objectType='collection', owner=user)
        rootNode.save()

        url = 'https://demo.pilvivayla.fi/api/cms/' + username

        ''' #TODO
        # Create new token
        token = Token.objects.create(user=user)
        key = token.key
        '''

        # Print everything to the user
        self.stdout.write('New CMS %s created!' % username)
        self.stdout.write('Username: %s' % username)
        self.stdout.write('Email:  %s' % email)
        self.stdout.write('Password:  %s' % password)
        self.stdout.write('-----------------------------------')
        self.stdout.write('API root-node:  %s' % url)
        #self.stdout.write('Token:  %s' % key)
        return 0