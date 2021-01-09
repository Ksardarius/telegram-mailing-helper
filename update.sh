#!/bin/bash -e

workdir=`dirname $0`
echo "Workdir: $workdir"
sudo service stop telegram-mailing-helper
echo "CURRENT VERSION: $(git -C $workdir/telegram-mailing-helper describe --tags --abbrev=0)"
git -C $workdir/telegram-mailing-helper pull || true
echo "list of available version:"
git -C $workdir/telegram-mailing-helper tag
read -p 'Please set update version: ' version
git -C $workdir/telegram-mailing-helper checkout $version
echo "Switch into version: $(git -C $workdir/telegram-mailing-helper describe --tags --abbrev=0)"
echo "Start..."
sudo service start telegram-mailing-helper
echo "Started... please check info! on 'http://host:port/info"
