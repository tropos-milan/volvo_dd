import pandas as pd
import getpass
from sqlalchemy import create_engine

class SnowflakeConnector:
    def __init__(self, account='volvocars-manufacturinganalytics',
                 user=f'{getpass.getuser()}@volvocars.com',
                 database='VCG', schema='INFORMATION_SCHEMA'):
        self.account = account
        self.user = user
        self.database = database
        self.schema = schema
        self.engine = None

    def create_engine(self):
        engine_url = (
            f"snowflake://{self.user}@{self.account}/"
            f"{self.database}/{self.schema}"
        )
        self.engine = create_engine(
            engine_url,
            connect_args={
                'user': self.user,
                'authenticator': 'externalbrowser',
            }
        )

    def query_data(self, query):
        if not self.engine:
            self.create_engine()

        with self.engine.connect() as connection:
            return pd.read_sql_query(query, connection)

    def close(self):
        if self.engine:
            self.engine.dispose()



