# 1. import Flask
from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my 'SQLAlchemy Challenge' page!<br/>"
        f"Routes that are available:<br/>" 
        f"/api/v1.0/precipitation: Return the JSON representation of your dictionary.<br/>"
        f"/api/v1.0/stations: Return a JSON list of stations from the dataset.<br/>"
        f"/api/v1.0/tobs: Return a JSON list of temperature observations (TOBS) for the previous year.<br/>"
        f"/api/v1.0/&#60;start&#62; and /api/v1.0/&#60;start&#62;/&#60;end&#62;: Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.<br/>"
    )

if __name__ == "__main__":
    app.run(debug=True)
