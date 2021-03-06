# Import Flask and needed Dependencies
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Create an app, being sure to pass __name__
app = Flask(__name__)

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my 'SQLAlchemy Challenge' page!<br/><br/>"
        f"Routes that are available:<br/>" 
        f"/api/v1.0/precipitation: Return the JSON representation of your dictionary.<br/>"
        f"/api/v1.0/stations: Return a JSON list of stations from the dataset.<br/>"
        f"/api/v1.0/tobs: Return a JSON list of temperature observations (TOBS) for the previous year.<br/>"
        f"/api/v1.0/&#60;start&#62; and /api/v1.0/&#60;start&#62;/&#60;end&#62;: Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.<br/>"
    )

# Define what to do when a user hits the "precipitation" route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in data set.
    last_year = dt.date(2017,8,23) - dt.timedelta(365)
    # Perform a query to retrieve the data and precipitation scores
    rain_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).order_by(Measurement.date).all()
    # Create a dictionary from the row data and append to a list
    prcp_values = []
    for p in rain_query:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        prcp_values.append(prcp_dict)
    return jsonify(prcp_values)

# Define what to do when a user hits the "stations" route
@app.route("/api/v1.0/stations")
def stations():
    # Perform a query to retrieve stations ID
    station_query = session.query(Station).all()
    # Create a dictionary from the row data and append to a list
    station_names = []
    for s in station_query:
        station_dict = {}
        station_dict["station"] = s.station
        station_dict["name"] = s.name
        station_names.append(station_dict)
    return jsonify(station_names)

# Define what to do when a user hits the "TOBS" route
@app.route("/api/v1.0/tobs")
def tobs():
    # Design a query to find the most active stations
    active_query = session.query(Measurement.station, func.count(Measurement.prcp)).group_by(Measurement.station).order_by(func.count(Measurement.prcp).desc()).all()
    most_active_id = active_query[0][0]
    # Calculate the date one year from the last date in data set.
    last_year = dt.date(2017,8,23) - dt.timedelta(365)
    # Perform a query to retrieve most active station TOBS.
    most_active_rain_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_id, Measurement.date >= last_year).order_by(Measurement.date).all()
    # Create a dictionary from the row data and append to a list
    tobs_values = []
    for t in most_active_rain_query:
        tobs_dict = {}
        tobs_dict["date"] = t.date
        tobs_dict["tobs"] = t.tobs
        tobs_values.append(tobs_dict)
    return jsonify(tobs_values)

# Define what to do when a user hits the "start" route
@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Set start and end dates for date range
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime("2017-08-23", "%Y-%m-%d")
    # Perform a query to retrieve temperature value in desired date.
    temp_query = session.query(Measurement.tobs).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    temp = [t[0] for t in temp_query]
    # Calculate the lowest, highest, and average temperature.
    lowest_temp = min(temp)
    avg_temp = np.mean(temp)
    highest_temp = max(temp)
    # Dictionary of temperatures
    temp_dict = {}
    temp_dict["Minimum Temperature (TMIN)"] = lowest_temp
    temp_dict["Average Temperature (TAVG)"] = avg_temp
    temp_dict["Maximum Temperature (TMAX)"] = highest_temp
    return jsonify(temp_dict)

# Define what to do when a user hits the "start-end" route
@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    # Set start and end dates for date range
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    # Perform a query to retrieve temperature value in desired date.
    temp_query = session.query(Measurement.tobs).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    temp = [t[0] for t in temp_query]
    # Calculate the lowest, highest, and average temperature.
    lowest_temp = min(temp)
    avg_temp = np.mean(temp)
    highest_temp = max(temp)
    # Dictionary of temperatures
    temp_dict = {}
    temp_dict["Minimum Temperature (TMIN)"] = lowest_temp
    temp_dict["Average Temperature (TAVG)"] = avg_temp
    temp_dict["Maximum Temperature (TMAX)"] = highest_temp
    return jsonify(temp_dict)


if __name__ == "__main__":
    app.run(debug=True)
