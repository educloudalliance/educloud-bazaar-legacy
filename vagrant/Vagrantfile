# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "ubuntu12.04"
  
  config.vm.network "forwarded_port", guest: 8069, host: 8069
  config.vm.provision :shell, :path => "odoo_install.sh"
  
  # Unless you change the user in the instal script 
  # (eg. for installing two DBs in parallel) 
  # this will sync the install dir to your host for easy inpection and editing
  config.vm.synced_folder "./odoo_src", "/opt/odoo_sync", create: true
end
