#!/bin/sh

# This shell script installs *static* Lua v5.4 libraries

echo "----------------------------------------------------------------------"
echo $0
echo "----------------------------------------------------------------------"
echo ""

mkdir -p /usr/local/installed

numCores=$(nproc)

extractTarFile() {
  echo "----------------------------------------------------------"
  cd /usr/local
  cp /tmp/artifacts/$2 installed
  mkdir -p /usr/local/src/$1
  tar xvf installed/$2            \
    --directory=/usr/local/src/$1 \
    --strip-components=1
  cd /usr/local/src/$1
  patch -p1 < /tmp/artifacts/lua.$1.patch
  echo "----------------------------------------------------------"
}

extractTarFile lua     lua.tar.gz
make -j $numCores
make install
cd /usr/local/lib

extractTarFile luaFileSystem     luaFileSystem.tar.gz
make -j $numCores
make install

extractTarFile luaSocket luaSocket.tar.gz
cd src
LUAV=5.4 make linux
LUAV=5.4 make install

extractTarFile luaCJson  luaCJson.tar.gz
make -j $numCores
make install
make install-extra

# extractTarFile luaDKJson luaDKJson
cd /usr/local
cp /tmp/artifacts/luaDKJson /usr/local/share/lua/5.4/dkjson

extractTarFile luaLunaJson luaLunaJson.tar.gz
cp -R src/* /usr/local/share/lua/5.4

extractTarFile luaUUID   luaUUID.tar.gz
cp src/uuid.lua /usr/local/share/lua/5.4/

extractTarFile luaNATS   luaNATS.tar.gz
cp src/nats.lua /usr/local/share/lua/5.4/

extractTarFile luaYAML   luaYAML.tar.gz
cp yaml.lua /usr/local/share/lua/5.4/

extractTarFile luaPPrint luaPPrint.tar.gz
cp pprint.lua /usr/local/share/lua/5.4/

# Make sure all shared libraries are indexed for ld.so
#
ldconfig
