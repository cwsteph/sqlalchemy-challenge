import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"  
        f"/api/v1.0/tobs<br/>"  
        f"/api/v1.0/temperature/start/end"
        )   


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    precip_data = session.query(measurement.date, measurement.prcp).all()

    # dates = [precip[0]for precip in precip_data]
    # rain = [precip[1]for precip in precip_data]

    combined = {date:prcp for date, prcp in precip_data}

    # results = {
    #     "date": dates,
    #     'precipitation' : rain
    # }

    session.close()

    """Return a list of all measurement values"""
    # Query all passengers
    # results = session.query(Passenger.name).all()
    # results = session.query(measurements.prcp).all()

    return jsonify(combined)




    # Convert list of tuples into normal list
    # all_names = list(np.ravel(results))

    # return jsonify(all_names)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    station_data = session.query(station.station).all()

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    # results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    tobs = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= '2016-08-23').all()

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    # results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    return jsonify(tobs)

@app.route("/api/v1.0/temperature/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start_end = session.query(func.min(measurement.tobs), 
              func.max(measurement.tobs), 
              func.avg(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    print(start_end)
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    # results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    return jsonify(start_end)


@app.route("/api/v1.0/temperature/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start = session.query(func.min(measurement.tobs), 
              func.max(measurement.tobs), 
              func.avg(measurement.tobs)).filter(measurement.date >= start).all()
   
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    # results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    return jsonify(start)

if __name__ == '__main__':
    app.run(debug=True)