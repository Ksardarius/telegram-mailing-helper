#!/bin/bash
cd `dirname $0`
PYTHONPATH=`pwd`/../ poetry run python ./main.py
