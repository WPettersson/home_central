#!/usr/bin/env python3
"""Read temperature at predefined intervals, and store to a database.
"""


from glob import glob
from time import sleep
from os import environ

import psycopg2


SLEEP_TIME = 60
"""Sleep time, in seconds."""


BASE_DIR = '/sys/bus/w1/devices/'
"""Base dir for w1 devices"""
DEVICE_FOLDER = glob(BASE_DIR + '28*')[0]
"""Glob to find the 1 wire device"""
DEVICE_FILE = DEVICE_FOLDER + '/w1_slave'
"""The actual device"""

# Read parameters from environment variables
DB = environ['HC_DB']
DBHOST = environ['HC_DBHOST']
USER = environ['HC_USER']
PASSWORD = environ['HC_PASSWORD']
ZONE = environ['HC_TEMP_ZONE']


def read_temp():
    """Reads a temperature, returning it in Celsius."""
    with open(DEVICE_FILE, "r") as devfile:
        crc = devfile.readline().split(' ')[-1].rstrip()
        if crc != "YES":
            return -1
        return int(devfile.readline().rsplit('t=')[-1].rstrip())


def store_temp(temp):
    """Store the temperature into a database."""
    conn = psycopg2.connect(dbname=DB, user=USER, password=PASSWORD,
                            host=DBHOST)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO temperatures (zone_id, temp)"
                   "VALUES (%s, %s)", (ZONE, temp))
    conn.commit()
    cursor.close()
    conn.close()


def main():
    """Main loop"""
    while True:
        temp = read_temp()
        # Don't store -1, which indicates sensor not ready.
        if temp != -1:
            try:
                store_temp(temp)
            except psycopg2.OperationalError as e:
                # Probably a database host not reachable problem, print it but
                # keep running
                print(e)
        sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
