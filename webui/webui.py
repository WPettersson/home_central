"""Web UI for home central"""

from flask import Flask, jsonify, render_template
import pandas
import psycopg2
from os import environ

app = Flask(__name__)

# Read parameters from environment variables
DB = environ['HC_DB']
USER = environ['HC_USER']
PASSWORD = environ['HC_PASSWORD']


def get_zones():
    """Get the names and ids of zones."""
    conn = psycopg2.connect(dbname=DB, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    cursor.execute("SELECT id, shortname FROM zones")
    data = cursor.fetchall()
    zones = [{'id': row[0], 'name': row[1]} for row in data]
    return zones


@app.route("/")
def main():
    """Display main screen."""
    return render_template('index.html')


@app.route("/temps/<hours>")
def get_temperatures(hours=24):
    """Get (recent) temperatures from a zone."""
    hours = int(hours)
    if hours > 168:
        raise Exception(f"Too large a duration passed: {hours}")
    sets = []
    all_zones = get_zones()
    conn = psycopg2.connect(dbname=DB, user=USER, password=PASSWORD)
    cursor = conn.cursor()
    for zone in all_zones:
        cursor.execute("SELECT temp, datestamp FROM temperatures "
                       "WHERE zone_id = %s "
                       "AND (NOW() - interval '%s hours') < datestamp",
                       (zone['id'], hours))
        data = cursor.fetchall()
        tempdata = [{'timestamp': row[1], 'temp': row[0]/1000}
                    for row in data]
        df = pandas.DataFrame(tempdata)
        df['timestamp'] = pandas.to_datetime(df['timestamp'])
        df = df.set_index('timestamp')
        myframe = pandas.DataFrame()
        if hours <= 24:
            myframe['temp'] = (df.temp.resample('15 min').mean()
                               .interpolate(method='linear'))
        elif hours <= 72:
            myframe['temp'] = (df.temp.resample('H').mean()
                               .interpolate(method='linear'))
        else:
            myframe['temp'] = (df.temp.resample('H').mean()
                               .interpolate(method='linear'))
        data = [{'timestamp': row[0],
                 'temp': row[1]} for row in zip(myframe.index.tolist(),
                                                myframe.temp.tolist())]
        sets.append({'label': zone['name'],
                     'data': data})
    cursor.close()
    conn.close()
    return jsonify(sets)


if __name__ == "__main__":
    app.run()
