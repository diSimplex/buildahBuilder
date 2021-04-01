#!/bin/sh

# This bin script finalizes the installation of the go language 

echo "----------------------------------------------------------------------"
echo $0
echo "----------------------------------------------------------------------"
echo ""

. $HOME/pdeVars

set -eux

mkdir -p $GOBIN
