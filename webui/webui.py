"""Web UI for home central"""

from flask import Flask, jsonify, render_template
import pandas
import psycopg2

from homecentral.db import DB

app = Flask(__name__)


def get_zones():
    """Get the names and ids of zones."""
    db = DB()
    cursor = db.cursor()
    cursor.execute("SELECT id, shortname FROM zones")
    data = cursor.fetchall()
    zones = [{'id': row[0], 'name': row[1]} for row in data]
    return zones


@app.route("/")
def main():
    """Display main screen."""
    return render_template('index.html')


@app.route("/temp/<zone>/<hours>")
def get_temperature_in_zone(zone=1, hours=24):
    """Get (recent) temperatures from a zone."""
    hours = int(hours)
    if hours > 2016:
        raise Exception(f"Too large a duration passed: {hours}")
    db = DB()
    cursor = db.cursor()
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
    elif hours <= 168:
        myframe['temp'] = (df.temp.resample('2H').mean()
                           .interpolate(method='linear'))
    elif hours <= 336:
        myframe['temp'] = (df.temp.resample('3H').mean()
                           .interpolate(method='linear'))
    elif hours <= 672:
        myframe['temp'] = (df.temp.resample('6H').mean()
                           .interpolate(method='linear'))
    else:
        myframe['temp'] = (df.temp.resample('D').mean()
                           .interpolate(method='linear'))
    data = [{'timestamp': row[0], 'temp': row[1]}
            for row in zip(myframe.index.tolist(), myframe.temp.tolist())]
    cursor.close()
    return jsonify({'label': zone['name'],
                    'data': data})


@app.route("/temps/<hours>")
def get_temperatures(hours=24):
    """Get (recent) temperatures from all zones."""
    hours = int(hours)
    if hours > 2016:
        raise Exception(f"Too large a duration passed: {hours}")
    sets = []
    db = DB()
    cursor = db.cursor()
    all_zones = get_zones()
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
        elif hours <= 168:
            myframe['temp'] = (df.temp.resample('2H').mean()
                               .interpolate(method='linear'))
        elif hours <= 336:
            myframe['temp'] = (df.temp.resample('3H').mean()
                               .interpolate(method='linear'))
        elif hours <= 672:
            myframe['temp'] = (df.temp.resample('6H').mean()
                               .interpolate(method='linear'))
        else:
            myframe['temp'] = (df.temp.resample('D').mean()
                               .interpolate(method='linear'))
        data = [{'timestamp': row[0],
                 'temp': row[1]} for row in zip(myframe.index.tolist(),
                                                myframe.temp.tolist())]
        sets.append({'label': zone['name'],
                     'data': data})
    cursor.close()
    return jsonify(sets)


if __name__ == "__main__":
    app.run()
