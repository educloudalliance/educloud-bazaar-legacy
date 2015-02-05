#!/usr/bin/env bash

### Start the Database

cd /home/vagrant/educloud-bazaar
python manage.py syncdb --noinput
python manage.py migrate

### Populate DB (not being used at the moment)

# From Oscar
# python manage.py oscar_populate_countries # Oscar 1.0
# From Bazaar
# python manage.py oscar_import_catalogue fixtures/*.csv
# python manage.py oscar_import_catalogue_images fixtures/images.tar.gz
# python manage.py clear_index --noinput
# python manage.py update_index catalogue

echo "You've been provisioned"