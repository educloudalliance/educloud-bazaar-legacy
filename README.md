# EduCloud Bazaar

Service and material distribution channel

EduCloud Bazaar is built on top of [Oscar framework](http://oscarcommerce.com/)
We actually use Oscar v0.7.3. Sources of its apps can be found in https://github.com/django-oscar/django-oscar/tree/releases/0.7/oscar/apps

The different servers where this system can be found installed are:

* __Test__ (for development and testing, access for the core team)
https://bazaardev.educloudalliance.org
* __Demo/Production__ (production version in the Pilot phase)
https://bazaar.educloudalliance.org

# Bazaar development environment

Bazaar development can be started using [Vagrant](https://www.vagrantup.com/). Vagrant sets up a whole VM over VirtualBox with all the dependencies that that the system requires already installed.

To setup vagrant and the DE perform the following steps:

1. Clone this repository with `git clone git@github.com:educloudalliance/educloud-bazaar.git && cd educloud-bazaar`

2. __Install Vagrant__ from their page. DO NOT USE `sudo apt-get install vagrant`, it installs an older version and it won't work. [Download Vagrant](https://www.vagrantup.com/downloads.html)

3. __Install VirtualBox__. You can either download it from [here](https://www.virtualbox.org/wiki/Downloads), or you can use `sudo apt-get install virtualbox virtualbox-dkms` in linux.

4. Uncomment the desired provisioning method from the `Vagrantfile` file:
  * __Provisioning from ansible:__ It will install everything from the cookbook located in `provision/ansible`. Make sure ansible is installed (it only works in MacOS and Linux)
  * __-->DEFAULT<-- Provisioning from *educloud-bazaar.box*:__ This will download our custom vagrant box from our server. This box has all the needed requirements preinstalled, so it's just run and code! It's really useful for CI and testing. It will be updated from time to time to meet the same requirements of the development and production server.
  * __Provisioning from bash script:__ This will download an empty virtual machine of Ubuntu 14.04 Precise Pangolin x64 and install all the requirements for you. It takes some time as it has to install everything.

5. Open a terminal in the root folder of the project and execute `vagrant up`. The first time you run this command will install a new VM in your computer with all the source code inside. If you chose the ansible or shwll script methods this will take some time, as it has to install the whole environment. It will also migrate and create the DB for you.

6. Now you can log in into your VM using `vagrant ssh`. All the source code is synced between the host and guest machine, so you can work from your own machine if desired. In order to start the educloud-bazaar service in the server execute `python /home/vagrant/educloud-bazaar/bazaar/manage.py runserver 0.0.0.0:8000`. You can access to the webpage through your browser at http://localhost:8001.

7. To stop the vagrant machine just use `vagrant halt` in the root folder. You an also destroy the whole machine with `vagrant destroy`. Next time it starts the machine it will provision again.

### Useful commands
* Generate and migrate the DB -->`python manage.py syncdb` and `python manage.py migrate`
* Start Unit tests --> `python manage.py test`
* Add CMS into the database (needs input) --> `python manage.py addcms [name]`
* Add LMS into the database (needs input) --> `python manage.py addlms [name]`

You can also see more commands of python using `python manage.py`

# Robot Framework tests

Location [educloud-bazaar/robot](https://github.com/koulutuksenpilvivayla/pilvivayla-basaari/tree/master/robot)

Required items:

* __robotframework__ `pip install robotframework`
* __selenium2library__ `pip install robotframework-selenium2library`
* __browser__ (firefox, chrome, ie, etc)

Example run, using [smoke.robot](https://github.com/educloudalliance/educloud-bazaar/blob/master/robot/smoke.robot):
`pybot --variable ENVIRONMENT:local_server --variable LANG:fi smoke.robot`

Currently if you run with ENVIRONMENT:local_server the test relys on your [local server that is running on port 8000](http://localhost:8000) and language depends on the browser default language.
