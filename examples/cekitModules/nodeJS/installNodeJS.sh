#!/bin/sh

# This bash setup script sets up the nvm nodeJS installer
#
# See: https://github.com/nvm-sh/nvm#git-install

echo "----------------------------------------------------------------------"
echo $0
echo "----------------------------------------------------------------------"
echo ""

. $HOME/pdeVars

echo ""

cd

git clone https://github.com/nvm-sh/nvm.git .nvm

echo ""

cd .nvm

git checkout v0.37.2

echo ""

. ./nvm.sh

echo ""

cat /tmp/artifacts/nvmBashrc >> $HOME/.bashrc

echo ""

# install the current LTS version of nodeJS
#
# See: https://nodejs.org/en/

#nvm install 12.18.1
 nvm install 14.16.0

npm install -g yarn

echo ""

echo "source $HOME/.nvm/nvm.sh" >> $HOME/.bashrc
