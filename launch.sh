#!/bin/bash

while true; do
    git pull
    python bot.py
    sleep 5
done


