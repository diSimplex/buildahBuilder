#!/bin/sh

# This bin script installs the go language 

echo "----------------------------------------------------------------------"
echo $0
echo "----------------------------------------------------------------------"
echo ""

. $HOME/pdeVars

set -eux

mkdir -p /usr/local/installed

cp -v /tmp/artifacts/goLang.tar /usr/local/installed

tar -C /usr/local -xzf /usr/local/installed/goLang.tar

recordVar PATH "/usr/local/go/bin:\$PATH"

go version

# The GOPATH is used as the download cache of `use`d go projects
recordVar GOPATH $HOME/go
mkdir -p $GOPATH

# using GOBIN as /commons/bin ensures that all go binaries we create 
# are accessible from outside the container.
recordVar GOBIN /commons/bin
mkdir -p $GOBIN

# We add GOBIN and GOPATH to the executable PATH
recordVar PATH \$GOBIN:\$GOPATH/bin:/usr/local/go/bin:\$PATH
