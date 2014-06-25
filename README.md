EduCloud Basaar
==================

Service and material distribution channel 

EduCloud Basaar is built on top of [Oscar framework](http://oscarcommerce.com/)

The site is deployed to two locations:

Demo
http://ip-193-166-24-116.hosts.forgeservicelab.fi/

Production (not yet)
http://basaar.pilvivayla.fi

Basaar development environment
------------------------------
Requirements: Virtualbox, Vagrant

Run "vagrant up" and have a coffee.

After installation, "vagrant ssh" to Virtualbox

cd basaar
python sites/basaar/manage.py runserver 0.0.0.0:8000

Open browser http://localhost:8000/

Voíla, you have Basaar Demo running locally!
