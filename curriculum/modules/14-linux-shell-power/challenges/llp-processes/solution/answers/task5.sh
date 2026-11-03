#!/bin/bash
./slow.sh A &
./slow.sh B &
wait
echo done
