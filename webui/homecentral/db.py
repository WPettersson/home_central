"""Database access"""

from os import environ
from time import sleep
import psycopg2
import psycopg2.extras


class DB:
    """Controls access to the database."""
    _conn = None
    _usage = 0

    def __init__(self):
        """If not connected, connect, else increase usage counter."""
        time_delay = 1
        while DB._conn is None:
            # Read parameters from environment variables
            try:
                DB._conn = psycopg2.connect(dbname=environ['HC_DB'],
                                            user=environ['HC_USER'],
                                            password=environ['HC_PASSWORD'],
                                            host=environ['HC_DBHOST'])
                psycopg2.extras.register_hstore(DB._conn)
                DB._usage = 1
            except psycopg2.OperationalError as exc:
                if "Temporary failure in name resolution" in exc.message:
                    sleep(time_delay)
                    if time_delay == 1:
                        time_delay = 5
                    elif time_delay == 5:
                        time_delay = 15
                    elif time_delay == 15:
                        time_delay = 45
                else:
                    raise exc
        DB._usage += 1

    def __del__(self):
        """Remove a user. If we're the last, close the connection."""
        DB._usage -= 1
        if DB._usage == 0:
            DB._conn.close()
            DB._conn = None

    def cursor(self):
        """Get a cursor to the DB"""
        return DB._conn.cursor()

    def commit(self):
        """Commit a transaction."""
        DB._conn.commit()


def get_zones():
    """Get the names and ids of zones."""
    db = DB()
    cursor = db.cursor()
    cursor.execute("SELECT id, shortname FROM zones")
    data = cursor.fetchall()
    zones = [{'id': row[0], 'name': row[1]} for row in data]
    return zones


def get_temp(zone):
    """Return the temperature in the given zone.
    """
    db = DB()
    cursor = db.cursor()
    cursor.execute("SELECT temp FROM temperatures where zone_id = %s "
                   "ORDER BY datestamp DESC LIMIT 1", zone)
    return int(cursor.fetchone()[0])
