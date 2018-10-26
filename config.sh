#!/bin/bash

# Run this script as root to set-up timer reminder
# funtionality

cp todo-timer.service /etc/systemd/system/
cp todo-timer.timer /etc/systemd/system/

systemctl enable todo-timer.service
systemctl enable todo-timer.timer


systemctl start todo-timer.service
systemctl start todo-timer.timer
