# home_central
Various bits and pieces of my home control

# Overview

Currently this is just doing some temperature monitoring. Future plans include controlling the heating, and then possible lights or other features.

# Hardware bits

Temperature logging is done from a raspberry pi with a DS18B20 thermal sensor attached via a 1-wire bus on GPIO.

# Contents of this repo

* The [relay cover](RelayCover/) that covers a relay that does nothing currently.
* The [Raspberry PI pinout](rpi-pinout.txt) that I'm using
* My [database schema](database-schema.txt)
* A [temperature logging](templogger/templogger.py) script
* A [web-based UI](webui/) to read temperatures
