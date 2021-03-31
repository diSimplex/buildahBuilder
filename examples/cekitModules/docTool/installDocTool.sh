#!/bin/sh

# This shell script installs the GoLang based docTool
#
# see: https://github.com/stephengaito/docTool
#

echo "----------------------------------------------------------------------"
echo $0
echo "----------------------------------------------------------------------"
echo ""

. /commons/pdeVars

cd ; mkdir -p tmp ; cd tmp

git clone https://github.com/stephengaito/docTool.git

cd docTool

go get

go install
