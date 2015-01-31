#!/usr/bin/env bash

# From Creating a Vagrant Box

cat << EOF | sudo tee -a /etc/motd.tail
***************************************

Welcome to precise64 Vagrant Box

For Bazaar development

***************************************
EOF

sudo sed -i 's/us/fi/' /etc/apt/sources.list
sudo apt-get update
sudo apt-get install -y python-software-properties
sudo apt-get update
sudo apt-get install -y git-core curl build-essential wget

### From Installing SQLite

sudo apt-get install -y sqlite3 libsqlite3-dev


### From Installing Apache

sudo apt-get install -y apache2 apache2-mpm-worker apache2-threaded-dev libapr1-dev libaprutil1-dev
sudo a2enmod rewrite
sudo service apache2 restart

### Disable default site
rm /etc/apache2/sites-enabled/000-default

### From Installing Java

sudo apt-get install -y openjdk-7-jdk

### From Installing Python

sudo apt-get install -y python-pip python-dev libjpeg-dev libfreetype6-dev zlib1g-dev
sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/libfreetype.so
sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/libjpeg.so
sudo ln -s /usr/lib/x86_64-linux-gnu/ibz.so /usr/lib/ibz.so

### Security

sudo apt-get install -y fail2ban mosh ufw
# Configure ufw
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8000
sudo ufw allow 8080
sudo echo 'y' | ufw enable


### Install Apache Solr

sudo apt-get install -y solr-tomcat

### Install oscar-django and other pip packages

cd ~
sudo pip install djangorestframework==2.3.14
sudo pip install django-oscar==0.7.2
sudo pip install django-json-field==0.5.5
sudo pip install django-rest-swagger==0.1.14
sudo pip install django-cookie-message==0.1
sudo pip install django-oauth2-provider==0.2.6.1
sudo pip install django-debug-toolbar-template-timings==0.6.4
sudo pip install pysolr==3.2.0
sudo pip install django-secure
sudo pip install django-extensions
sudo pip install django-autoslug
sudo pip install html2text

### Start the Database

cd /home/vagrant/educloud-bazaar/bazaar
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