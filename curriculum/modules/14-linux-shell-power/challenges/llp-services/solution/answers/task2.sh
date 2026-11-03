#!/bin/bash
curl -s "http://127.0.0.1:$(cat port.txt)/status.txt"
