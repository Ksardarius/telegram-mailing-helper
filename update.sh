#!/bin/bash -e

workdir=`dirname $0`
echo "Workdir: $workdir"
echo "Try to stop service..."
sudo service telegram-mailing-helper stop
echo "CURRENT VERSION: $(git -C $workdir describe --tags --abbrev=0)"
git -C $workdir pull || true
echo "list of available version:"
git -C $workdir tag
read -p 'Please set update version: ' version
git -C $workdir checkout $version
echo "Switch into version: $(git -C $workdir describe --tags --abbrev=0)"
echo "Update project dependencies..."
cd $workdir
poetry install
echo "Start..."
sudo service telegram-mailing-helper start
echo "Started... please check info! on 'http://host:port/info"
