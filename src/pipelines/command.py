import pandas as pd

from src.database.postgres import StocksDatabase
from src.models.stocks import Base
from sqlalchemy.sql import text

class DatabaseSetup:
    """
    Part 1: Database Setup and Data Ingestion
    """

    @staticmethod
    def run(dataframe: pd.DataFrame, table: Base):
        with StocksDatabase(conn=None, session=None, engine='sqlalchemy') as database:
            database.execute(text(
                    f"""SELECT create_hypertable('{table.__tablename__}', 
                                '{table.__hypertable_field__}', 
                                if_not_exists => TRUE)"""))

            for index, row in dataframe.iterrows():
                data = table(**row)
                database.add(data)


class Querying:
    """
    Part 2: Querying and Data Manipulation
    """

    @staticmethod
    def run(table: Base):
        with StocksDatabase(conn=None, session=None, engine='psycopg2') as database:

            query = f"""
            SELECT date, ticker, volume FROM 
                (SELECT
                    ticker,
                    date,
                    volume,
                    ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY volume DESC) AS row_num
                FROM
                    {table.__tablename__}) AS inner_query
                WHERE row_num = 1;
            """

            df = pd.read_sql_query(query, database.conn)
            df.to_csv('./highest_volume_day.csv', encoding='utf-8', index=False)

        with StocksDatabase(conn=None, session=None, engine='psycopg2') as database:
            query = f"""
            SELECT 
                time_bucket('7 days', date::timestamp) AS seven_days_bucket,
                ticker,
                AVG(close) seven_days_avg
            FROM 
                {table.__tablename__}
                GROUP BY 1, 2
                ORDER BY 1 ASC, 2 DESC;
            """

            df = pd.read_sql_query(query, database.conn)
            df.to_csv('./avg_by_week.csv', encoding='utf-8', index=False)

        with StocksDatabase(conn=None, session=None, engine='psycopg2') as database:
            query = f"""
            SELECT 
                date, 
                ticker, 
                close,
                close - LAG(close, 1) OVER (ORDER BY date, ticker) AS price_change
            FROM 
                {table.__tablename__}
                ORDER BY 2, 4 DESC
            """

            df = pd.read_sql_query(query, database.conn)
            df.to_csv('./price_change.csv', encoding='utf-8', index=False)



