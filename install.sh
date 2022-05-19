#!/usr/bin/env bash

#Update
apt update
#Install PiHole
sudo curl -sSL https://install.pi-hole.net | bash

#Install PM2
apt install sudo curl && curl -sL https://raw.githubusercontent.com/Unitech/pm2/master/packager/setup.deb.sh | sudo -E bash -

#Install needed python packages
sudo pip install -r ./requirements.txt