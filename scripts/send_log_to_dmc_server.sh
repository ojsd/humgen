#!/usr/bin/env bash
# This is a script used to transfer data log files and debug log files to Dome C server.
#
# It uses a SSH connection, and assumes that this connection is already successfully established between the RaspberryPi
# and dmc server.
# It also assumes that no password is required to connect to dmc_server, meaning that the authentication mechanism using
# RSA keys has been set up. See this page for example:
# https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2
#
# Server url, from Internet: hermes.enea.pnra.it
# Server url, from Dome C: hermes2.concordiastation.aq
# User: nivo_dmc
# Distant folder: /home/projects/nivo_dmc/from_dmc/isotope

# Copy log files to temporary folder
cp /home/pi/Documents/Calib/log/* /home/pi/Documents/_to_send/

# Zip all log files
gzip -rf /home/pi/Documents/_to_send/*

# Send files to server
## When used from internet -- FOR TESTS ONLY
# scp -r /home/pi/Documents/Calib/log nivo_dmc@hermes.enea.pnra.it:/home/projects/nivo_dmc/from_dmc/isotope
## When used from Dome C
scp -r /home/pi/Documents/Calib/log nivo_dmc@hermes2.concordiastation.aq:/home/projects/nivo_dmc/from_dmc/isotope

# Remove uncompressed files older than 10 days
find /home/pi/Documents/Calib/log -name "*.log" -mtime +10 -type f -delete