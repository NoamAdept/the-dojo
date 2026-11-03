#!/bin/bash
sed -i "s/^port=.*/port=$(cat new_port.txt)/" beacon.conf
./ctl.sh restart
