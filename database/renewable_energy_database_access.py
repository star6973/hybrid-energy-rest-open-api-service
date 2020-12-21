import sqlalchemy
from sqlalchemy import create_engine, and_, Column, Integer, String, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
# from database.renewable_energy_database_by_day import Energy
from sqlalchemy_utils import JSONType

Base = declarative_base()
DBSession = scoped_session(sessionmaker())


class Energy_day(Base):
    __tablename__ = "Renewable_Energy_By_Day"
    # 파이썬 객체 생성
    id = Column(Integer, primary_key=True)
    Administrative_Area = Column(String)
    Observation = Column(String)

    P_pv = Column(JSONType)
    P_wind = Column(JSONType)
    P_load = Column(JSONType)

    Optimal_prompt1 = Column(FLOAT)
    Optimal_prompt2 = Column(FLOAT)
    Optimal_cost = Column(FLOAT)

    Optimal_p_wind = Column(JSONType)
    Optimal_p_dummy = Column(JSONType)
    Optimal_p_pv = Column(JSONType)
    Optimal_p_battery = Column(JSONType)
    Optimal_p_load = Column(JSONType)
    Optimal_soc = Column(JSONType)
    Optimal_p_dg = Column(JSONType)
    Optimal_lolp = Column(JSONType)


class Energy_month(Base):
    __tablename__ = "Renewable_Energy_By_Month"
    # 파이썬 객체 생성
    id = Column(Integer, primary_key=True)
    Administrative_Area = Column(String)
    Observation = Column(String)

    P_pv = Column(JSONType)
    P_wind = Column(JSONType)
    P_load = Column(JSONType)

    Optimal_prompt1 = Column(FLOAT)
    Optimal_prompt2 = Column(FLOAT)
    Optimal_cost = Column(FLOAT)

    Optimal_p_wind = Column(JSONType)
    Optimal_p_dummy = Column(JSONType)
    Optimal_p_pv = Column(JSONType)
    Optimal_p_battery = Column(JSONType)
    Optimal_p_load = Column(JSONType)
    Optimal_soc = Column(JSONType)
    Optimal_p_dg = Column(JSONType)
    Optimal_lolp = Column(JSONType)


class Energy_year(Base):
    __tablename__ = "Renewable_Energy_By_Year"
    # 파이썬 객체 생성
    id = Column(Integer, primary_key=True)
    Administrative_Area = Column(String)
    Observation = Column(String)

    P_pv = Column(JSONType)
    P_wind = Column(JSONType)
    P_load = Column(JSONType)

    Optimal_prompt1 = Column(FLOAT)
    Optimal_prompt2 = Column(FLOAT)
    Optimal_cost = Column(FLOAT)

    Optimal_p_wind = Column(JSONType)
    Optimal_p_dummy = Column(JSONType)
    Optimal_p_pv = Column(JSONType)
    Optimal_p_battery = Column(JSONType)
    Optimal_p_load = Column(JSONType)
    Optimal_soc = Column(JSONType)
    Optimal_p_dg = Column(JSONType)
    Optimal_lolp = Column(JSONType)


class EnergyDatabase:
    def __init__(self):
        engine = create_engine('sqlite:///database/renewable_energy_database.db', echo=False)
        DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)

    def readByDay(self, date, area):
        energy = DBSession.query(Energy_day).filter(and_(Energy_day.Observation == date, Energy_day.Administrative_Area == area)).first()

        result = {}
        if energy is not None:
            result = {
                'Administrative_Area' : energy.Administrative_Area,
                'Observation' : energy.Observation,
                'P_pv' : energy.P_pv,
                'P_wind' : energy.P_wind,
                'P_load' : energy.P_load,
                'Optimal_prompt1' : energy.Optimal_prompt1,
                'Optimal_prompt2' : energy.Optimal_prompt2,
                'Optimal_cost' : energy.Optimal_cost,
                'Optimal_soc' : energy.Optimal_soc,
                'Optimal_p_wind' : energy.Optimal_p_wind,
                'Optimal_p_dummy' : energy.Optimal_p_dummy,
                'Optimal_p_pv' : energy.Optimal_p_pv,
                'Optimal_p_battery' : energy.Optimal_p_battery,
                'Optimal_p_load' : energy.Optimal_p_load,
                'Optimal_p_dg' : energy.Optimal_p_dg,
                'Optimal_p_lolp' : energy.Optimal_lolp
            }
            return result
        else:
            return None

    def readByMonth(self, date, area):
        energy = DBSession.query(Energy_month).filter(and_(Energy_month.Observation == date, Energy_month.Administrative_Area == area)).first()
        result = {}

        if energy is not None:
            result = {
                'Administrative_Area' : energy.Administrative_Area,
                'Observation' : energy.Observation,
                'P_pv' : energy.P_pv,
                'P_wind' : energy.P_wind,
                'P_load' : energy.P_load,
                'Optimal_prompt1' : energy.Optimal_prompt1,
                'Optimal_prompt2' : energy.Optimal_prompt2,
                'Optimal_cost' : energy.Optimal_cost,
                'Optimal_soc' : energy.Optimal_soc,
                'Optimal_p_wind' : energy.Optimal_p_wind,
                'Optimal_p_dummy' : energy.Optimal_p_dummy,
                'Optimal_p_pv' : energy.Optimal_p_pv,
                'Optimal_p_battery' : energy.Optimal_p_battery,
                'Optimal_p_load' : energy.Optimal_p_load,
                'Optimal_p_dg' : energy.Optimal_p_dg,
                'Optimal_p_lolp' : energy.Optimal_lolp
            }
            return result
        else:
            return None


    def readByYear(self, date, area):

        print(date)
        print(area)
        energy = DBSession.query(Energy_year).filter(and_(Energy_year.Observation == date, Energy_year.Administrative_Area == area)).first()
        print(DBSession.query(Energy_year).filter(and_(Energy_year.Observation == date, Energy_year.Administrative_Area == area)))
        result = {}

        if energy is not None:
            result = {
                'Administrative_Area' : energy.Administrative_Area,
                'Observation' : energy.Observation,
                'P_pv' : energy.P_pv,
                'P_wind' : energy.P_wind,
                'P_load' : energy.P_load,
                'Optimal_prompt1' : energy.Optimal_prompt1,
                'Optimal_prompt2' : energy.Optimal_prompt2,
                'Optimal_cost' : energy.Optimal_cost,
                'Optimal_soc' : energy.Optimal_soc,
                'Optimal_p_wind' : energy.Optimal_p_wind,
                'Optimal_p_dummy' : energy.Optimal_p_dummy,
                'Optimal_p_pv' : energy.Optimal_p_pv,
                'Optimal_p_battery' : energy.Optimal_p_battery,
                'Optimal_p_load' : energy.Optimal_p_load,
                'Optimal_p_dg' : energy.Optimal_p_dg,
                'Optimal_p_lolp' : energy.Optimal_lolp
            }
            return result
        else:
            return None
