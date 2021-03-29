#!/bin/sh

# This shell script installs the gccLang codeDocServer

echo "----------------------------------------------------------------------"
echo $0
echo "----------------------------------------------------------------------"
echo ""

mkdir -p $HOME/bin

cp /tmp/artifacts/codeDocServer $HOME/bin

chmod a+x $HOME/bin/codeDocServer
