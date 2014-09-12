EduCloud Basaar
==================

Service and material distribution channel 

EduCloud Basaar is built on top of [Oscar framework](http://oscarcommerce.com/)

The site is deployed to two locations:

Demo
http://demo.pilvivayla.fi

Production (not yet)
http://basaar.pilvivayla.fi

Basaar development environment
------------------------------
Requirements: Virtualbox , Vagrant , Git. In Ubuntu all can be installed via Software center.

* Clone repository "git clone git@github.com:koulutuksenpilvivayla/pilvivayla-basaari.git"
* Go to repository folder "pilviväylä-basaari" and 
* Run "vagrant up" and have a coffee.
* After installation, "vagrant ssh" to Virtualbox
* cd basaar && python sites/basaar/manage.py runserver 0.0.0.0:8000
* Open browser [http://localhost:8000/](http://localhost:8000)
* Voíla, you have Basaar Demo running locally!
* After this you need to update your local repository now and then to keep it updated by issuing command "git pull" inside the repository (folder)

## Robot Framework tests

Location [pilvivayla-basaari/robot](https://github.com/koulutuksenpilvivayla/pilvivayla-basaari/tree/devel/robot)

Required items:

* robotframework `pip install robotframework`
* selenium2library `pip install robotframework-selenium2library`
* browser (firefox, chrome, ie, etc)

Example run, using [smoke.robot](https://github.com/koulutuksenpilvivayla/pilvivayla-basaari/blob/devel/robot/smoke.robot):
`pybot --variable ENVIRONMENT:local_server --variable LANG:fi smoke.robot`

Currently if you run with ENVIRONMENT:local_server the test relys on your [local server that is running on port 8000](http://localhost:8000) and language depends on the browser default language.
