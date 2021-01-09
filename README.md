# telegram-mailing-helper
## Pre requirements
```shell
apt install python3-pip build-essential libsystemd-dev git
pip3 install poetry
```
## Installation (example)
- clone repo from github into /opt:
```shell
WORKDIR=/opt
sudo mkdir $WORKDIR
sudo chown $USER:$USER $WORKDIR/telegram-mailing-helper
cd /opt
git clone https://github.com/11sanach11/telegram-mailing-helper.git
cd telegram-mailing-helper
poetry install
cp ./test_config.json ./config.json
<<<!!! PREPARE CONFIG FILE, SET server.port, telegramToken, etc...
cp ./template_for_service/telegram-mailing-helper.service /etc/systemd/system/telegram-mailing-helper.service
sudo sed -i -e "s/%USER%/$USER/g" -e "s/%WORKDIR%/$WORKDIR/g" /etc/systemd/system/telegram-mailing-helper.service
sudo systemctl enable telegram-mailing-helper
$WORKDIR/update.sh
```

## UPDATE
```shell
telegram-mailing-helper
$WORKDIR/update.sh
```
