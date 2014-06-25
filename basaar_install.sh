#!/bin/bash
################################################################################
# Script for Installation: Basaar master/devel on Ubuntu 12.04 LTS
# Author: Ville Jyrkkä, Sampo Software Oy
#-------------------------------------------------------------------------------
# This script will install Basaar on
# clean Ubuntu 12.04 Server
#-------------------------------------------------------------------------------
# USAGE:
#
# ./basaar-install.sh
#
################################################################################

##fixed parameters
#basaar
BASAAR_USER="vagrant"
BASAAR_HOME="/home/$BASAAR_USER/basaar"

#Enter version for checkout "devel" for development and "master" for production
BASAAR_VERSION="devel"

#--------------------------------------------------
# Update Server
#--------------------------------------------------
echo -e "\n---- Update Server ----"
sudo apt-get update
sudo apt-get upgrade -y

#--------------------------------------------------
# Install Dependencies
#--------------------------------------------------
echo -e "\n---- Install tool packages ----"
sudo apt-get install git python-pip python-dev libjpeg-dev libfreetype6-dev zlib1g-dev -y

echo -e "\n---- Symlink image libraries ----"
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/

#--------------------------------------------------
# Install Oscar
#--------------------------------------------------
echo -e "\n==== Installing Basaar development environment ===="
echo -e "\nBe patient, next step takes a while, go and grab some coffee :)"
sudo git clone --branch $BASAAR_VERSION https://www.github.com/koulutuksenpilvivayla/pilvivayla-basaari $BASAAR_HOME/

echo -e "\n---- Installing basaar ----"
cd $BASAAR_HOME && sudo make basaar install

echo -e "\n---- Setting permissions on home folder ----"
sudo chown -R $BASAAR_USER:$BASAAR_USER $BASAAR_HOME/*

echo "Done! Basaar installed successfully!"
