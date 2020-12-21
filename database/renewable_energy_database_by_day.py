import sys
sys.path.append("../pso_algorithm")
import pso_algorithm_by_day
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, FLOAT, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import JSONType

Base = declarative_base()
DBSession = scoped_session(sessionmaker())

class Energy(Base):
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

def init_sqlalchemy(dbname = 'sqlite:///renewable_energy_database.db'):
    engine  = create_engine(dbname, echo=False)
    DBSession.configure(bind=engine, autoflush=False, expire_on_commit=False)
    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    return DBSession

def main():

    # 재생에너지 데이터 확보
    renewable_energy = pso_algorithm_by_day.get_renewable_energy() # DataFrame 형태
    init_sqlalchemy()

    # INSERT (POST)
    print("\n### db_session.add()")
    for idx in range(len(renewable_energy)):
        energy = Energy()

        energy.Administrative_Area = renewable_energy['Administrative_Area'][idx]
        energy.Observation = renewable_energy['Observation'][idx]

        energy.P_pv = renewable_energy['P_pv'][idx]
        energy.P_wind = renewable_energy['P_wind'][idx]
        energy.P_load = renewable_energy['P_load'][idx]

        energy.Optimal_prompt1 = renewable_energy['optimal_prompt1'][idx]
        energy.Optimal_prompt2 = renewable_energy['optimal_prompt2'][idx]
        energy.Optimal_cost = renewable_energy['optimal_cost'][idx]

        energy.Optimal_p_wind = renewable_energy['optimal_p_wind'][idx]
        energy.Optimal_p_dummy = renewable_energy['optimal_p_dummy'][idx]
        energy.Optimal_p_pv = renewable_energy['optimal_p_pv'][idx]
        energy.Optimal_p_battery = renewable_energy['optimal_p_battery'][idx]
        energy.Optimal_p_load = renewable_energy['optimal_p_load'][idx]
        energy.Optimal_soc = renewable_energy['optimal_soc'][idx]
        energy.Optimal_p_dg = renewable_energy['optimal_p_dg'][idx]
        energy.Optimal_lolp = renewable_energy['optimal_lolp'][idx]

        DBSession.add(energy) # 객체(테이블)를 만들고 추가하기

    DBSession.commit()

    count = DBSession.query(Energy).count()
    print("### There are {0} rows in the table after performing 'add'.".format(count))

if __name__ == '__main__':
    main()