EduCloud Bazaar
==================

Service and material distribution channel 

EduCloud Bazaar is built on top of [Oscar framework](http://oscarcommerce.com/)

The locations this site is deployed:

Test (for development and testing)
https://test.pilvivayla.fi

Demo (production version in the Pilot phase)
https://demo.pilvivayla.fi

Production (in the future, currently points to Demo)
https://bazaar.pilvivayla.fi

Bazaar development environment
------------------------------

Instructions and scripts for setting up Bazaar development environment is described in [pilvivayla-provisioning](https://github.com/koulutuksenpilvivayla/pilvivayla-provisioning).

## Robot Framework tests

Location [pilvivayla-basaari/robot](https://github.com/koulutuksenpilvivayla/pilvivayla-basaari/tree/devel/robot)

Required items:

* robotframework `pip install robotframework`
* selenium2library `pip install robotframework-selenium2library`
* browser (firefox, chrome, ie, etc)

Example run, using [smoke.robot](https://github.com/koulutuksenpilvivayla/pilvivayla-basaari/blob/devel/robot/smoke.robot):
`pybot --variable ENVIRONMENT:local_server --variable LANG:fi smoke.robot`

Currently if you run with ENVIRONMENT:local_server the test relys on your [local server that is running on port 8000](http://localhost:8000) and language depends on the browser default language.
