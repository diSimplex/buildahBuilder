#!/bin/sh

# This bin script installs the micro editor (and reWrapText plugin)

mkdir -p /usr/local/installed

cd /usr/local

cp /tmp/artifacts/micro.tar           installed

cp /tmp/artifacts/microReWrapText.tar installed

mkdir -p /usr/local/micro

tar xvf installed/micro.tar \
  --directory=/usr/local/micro   \
  --strip-components=1

mkdir -p /usr/local/micro/reWrapText

tar xvf installed/microReWrapText.tar \
  --directory=/usr/local/micro/reWrapText  \
  --strip-components=1

cd /usr/local/bin

ln -f -s /usr/local/micro/micro .

# This bash script setups the micro editor environment
#
# NOTE: this SHOULD be run as the dev user

cd /usr/local/micro/reWrapText

./bin/install
