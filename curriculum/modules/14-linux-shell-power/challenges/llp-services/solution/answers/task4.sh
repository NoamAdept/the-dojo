#!/bin/bash
grep 'listening on' service.log | tail -n 1 | awk -F: '{print $NF}'
