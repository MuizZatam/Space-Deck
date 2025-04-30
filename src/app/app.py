from flask import (
    
    Flask,
    render_template
)
from modules.Earth.earth_computes import computes
import datetime

app = Flask(__name__)


@app.route("/", methods = ["POST", "GET"])
def index():

    date = datetime.datetime.today()
    date = date.strftime(r"%d-%m-%Y")

    earth_observations = get_data_earth()


    return render_template("index.html", date = date, data = earth_observations)


def get_data_earth():

    return computes()


if __name__ == "__main__":

    app.run(debug=True)