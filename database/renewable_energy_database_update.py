import sqlite3

update_resource = """
    UPDATE Renewable_Energy_By_Year SET Optimal_prompt2=?, Optimal_cost=? WHERE Administrative_Area=? and Observation=?
"""

delete_resource = """
    DELETE FROM Renewable_Energy_By_Year WHERE Administrative_Area = ? and Observation=?
"""

selection_resource_by_administrative_area = """
    SELECT * FROM Renewable_Energy_By_Year WHERE Administrative_Area=?
"""

class RenewableEnergySourceDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('renewable_energy_database.db')

    def update(self, Administrative_Area, Observation, Optimal_prompt2, Optimal_cost):
        cur = self.conn.cursor()
        cur.execute(
            update_resource, (Optimal_prompt2, Optimal_cost, Administrative_Area, Observation)
        )
        self.conn.commit()

    def delete(self, Administrative_Area, Observation):
        cur = self.conn.cursor()
        cur.execute(
            delete_resource, (Administrative_Area, Observation)
        )
        self.conn.commit()

    def readByAdministrativeArea(self, Administrative_Area):
        cur = self.conn.cursor()
        cur.execute(
            selection_resource_by_administrative_area, (Administrative_Area,)
        )
        row = cur.fetchone()
        if row is not None:
            energy = {
                "id": row[0],
                "Administrative_Area": row[1],
                "Observation": row[2],
                "P_pv": row[3],
                "P_wind": row[4],
                "P_load": row[5],
                "optimal_prompt1": row[6],
                "optimal_prompt2": row[7],
                "optimal_cost": row[8],
                "optimal_p_wind": row[9],
                "optimal_p_dummy": row[10],
                "optimal_p_pv": row[11],
                "optimal_p_battery": row[12],
                "optimal_p_load": row[13],
                "optimal_soc": row[14],
                "optimal_p_dg": row[15],
                "optimal_lolp": row[16],
            }
        else:
            energy = None
        self.conn.commit()
        return energy


resd = RenewableEnergySourceDatabase()
resd.update('부산광역시', '2017', 4.0, 32308.0)
resd.update('부산광역시', '2018', 6.4, 42388.0)