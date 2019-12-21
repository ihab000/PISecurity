#!/bin/bash

sudo ps aux | pgrep -f "\\bPISecurityv4.py\\b" | xargs kill -9
#sudo su killall python3
