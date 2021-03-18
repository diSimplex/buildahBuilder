#!/bin/sh

# This shell script installs the gccLang codeDocServer

mkdir -p $HOME/bin

cp /tmp/artifacts/codeDocServer $HOME/bin

chmod a+x $HOME/bin/codeDocServer

#systemctl stop    webfs
#systemctl disable webfs
