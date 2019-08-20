# /Bootstraping/


#!/usr/bin/env bash

# PostgreSQL and PostGIS
apt-get -y update
apt-get -y install postgresql-11 postgresql-11-postgis-2.5 postgis postgresql-11-pgrouting gdal-bin osm2pgsql libpq-dev postgresql-client-11

# ZSH
apt-get install curl zsh git sqlite3
chsh -s /bin/zsh vagrant

# pyenv
apt-get -y install --no-install-recommends make build-essential libssl-dev zlib1g-dev\
                    libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev\
                    xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
