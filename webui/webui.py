"""Web UI for home central"""

from flask import Flask, jsonify, render_template
import psycopg2
from os import environ

app = Flask(__name__)

# Read parameters from environment variables
DB = environ['HC_DB']
USER = environ['HC_USER']
PASSWORD = environ['HC_PASSWORD']


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/temps/<zone>/<hours>")
def get_temperatures(zone=1, hours=24):
    """Get (recent) temperatures from a zone."""
    hours = int(hours)
    zone = int(zone)
    if hours > 24:
        raise Exception(f"Too large a duration passed: {hours}")
    conn = psycopg2.connect(dbname=DB, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute("SELECT temp, datestamp FROM temperatures "
                   "WHERE zone_id = %s "
                   "AND (NOW() - interval '%s hours') < datestamp",
                   (zone, hours))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([{'timestamp': row[1], 'temp': row[0]/1000}
                    for row in data])


if __name__ == "__main__":
    app.run()
