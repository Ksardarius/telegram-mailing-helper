#!/bin/bash -e

workdir=`dirname $0`
echo "Workdir: $workdir"
sudo service telegram-mailing-helper stop
echo "CURRENT VERSION: $(git -C $workdir/telegram-mailing-helper describe --tags --abbrev=0)"
git -C $workdir/telegram-mailing-helper pull || true
echo "list of available version:"
git -C $workdir/telegram-mailing-helper tag
read -p 'Please set update version: ' version
git -C $workdir/telegram-mailing-helper checkout $version
echo "Switch into version: $(git -C $workdir/telegram-mailing-helper describe --tags --abbrev=0)"
echo "Start..."
sudo service telegram-mailing-helper start
echo "Started... please check info! on 'http://host:port/info"
