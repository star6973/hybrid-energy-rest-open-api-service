from flask import Flask, render_template
from flask_restful import Api

from rest_client.example import example_blueprint
from rest_client.execute import execute_blueprint
from rest_server.rest_energy import EnergyDayResource, EnergyMonthResource, EnergyYearResource

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '12345678'
app.register_blueprint(execute_blueprint, url_prefix='/execute')
app.register_blueprint(example_blueprint, url_prefix='/example')

api = Api(app)
api.add_resource(EnergyDayResource, "/day-energy/<date>/area/<area>")
api.add_resource(EnergyMonthResource, "/month-energy/<date>/area/<area>")
api.add_resource(EnergyYearResource, "/year-energy/<date>/area/<area>")

@app.route('/manual')
def manual():
    return render_template(
        'manual.html',
        menu='manual'
    )

@app.route('/')
def hello_html():
    return render_template(
        'index.html',
        menu='main',
    )

if __name__ == "__main__":

    app.debug = True
    app.config['DEBUG'] = True
    app.run(host="localhost", port="5000")
