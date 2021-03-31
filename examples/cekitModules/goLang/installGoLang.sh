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

mkdir -p /commons/go

recordVar GOPATH /commons/go
recordVar GOBIN /commons/bin
recordVar PATH \$GOBIN:\$GOPATH/bin:/usr/local/go/bin:\$PATH
