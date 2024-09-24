from sqlalchemy import Column
from sqlalchemy.types import String, DateTime, Numeric
from sqlalchemy.dialects.mysql import INTEGER
# sqlalchemyのデータ型については以下を参照
# https://docs.sqlalchemy.org/en/14/dialects/mysql.html?highlight=unsigned#mysql-mariadb-specific-index-options

from setting import Base, Engine, session

class CO2SensorEdge(Base):
    """
    CO2センサを搭載したエッジデバイスから取得したデータ

    Args:
        Base (DeclarativeBase): sqlalchemyの基底クラス

    Attributes:
        timestamp (datetime)    : データ送信日時
        data_source (str)       : データのソースとなる機器名
        co2 (float)             : co2の値[ppm]
        temperature (float)     : 温度[℃]
    """
  
    __tablename__ = 'co2sensor_edge' # テーブル名
    __table_args__ = {'extend_existing': True,"mysql_charset": "utf8mb4"} # テーブル定義時に実行で再定義可
  
    # カラム名
    data_id       = Column(INTEGER(unsigned=True), nullable=False, autoincrement=True, primary_key=True) 
    timestamp     = Column(DateTime, nullable=False)
    data_source   = Column(String(255), nullable=False)
    co2           = Column(Numeric(10, 2))
    temperature   = Column(Numeric(10, 2))

    def create_record(
            self,
            timestamp,
            data_source,
            co2,
            temperature
            ):
        self.timestamp = timestamp
        self.data_source = data_source
        self.co2 = co2
        self.temperature = temperature


if __name__ == '__main__':
    try:
        print('create tables start')
        Base.metadata.create_all(bind=Engine)
    except:
        print('exception occur')
        session.rollback()
        raise
    finally:
        print('fin')
        session.close()