from flask_restful import Resource, reqparse, abort

from database.renewable_energy_database_access import EnergyDatabase


class EnergyDayResource(Resource):
    def __init__(self):
        self.Energy_resource_db = EnergyDatabase()
        # self.parser = reqparse.RequestParser()
        # self.parser.add_argument('day')
        # self.parser.add_argument('month')
        # self.parser.add_argument('year')

    def get(self, date, area):
        energy = self.Energy_resource_db.readByDay(date=date, area=area)
        if energy is None:
            abort(404, message="Wrong date")
        else:
            return energy, 200


class EnergyMonthResource(Resource):
    def __init__(self):
        self.Energy_resource_db = EnergyDatabase()

    def get(self, date, area):
        energy = self.Energy_resource_db.readByMonth(date = date, area=area)
        if energy is None:
            abort(404, message="Wrong date")
        else:
            return energy, 200


class EnergyYearResource(Resource):
    def __init__(self):
        self.Energy_resource_db = EnergyDatabase()

    def get(self, date, area):
        energy = self.Energy_resource_db.readByYear(date = date, area=area)
        if energy is None:
            abort(404, message="Wrong date")
        else:
            return energy, 200

