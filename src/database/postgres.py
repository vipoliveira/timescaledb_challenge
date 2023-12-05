import psycopg2
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.models.stocks import Base
from dataclasses import dataclass
from src.conf.env import Settings

class StocksDatabase:

    @staticmethod
    def connect(engine, **kwargs):
        if engine == 'psycopg2':
            return psycopg2.connect(**kwargs)

        elif engine == 'sqlalchemy':
            dbname = kwargs.get('dbname')
            user = kwargs.get('user')
            password = kwargs.get('password')
            host = kwargs.get('host')

            _engine = create_engine(
                f'postgresql://{user}:{password}@{host}:5432/{dbname}', echo=True)

            Base.metadata.create_all(_engine)
            session = sessionmaker(bind=_engine)()

            return session

    def __init__(self, conn, session, engine='psycopg2'):
        self.conn = conn
        self.session = session
        self.engine = engine
        self.cur = self.conn.cursor() if self.conn and self.engine == 'psycopg2' else None
        self.settings = Settings()

    def __enter__(self):
        self.conn = StocksDatabase.connect(
            engine=self.engine,
            dbname=self.settings.POSTGRES_DBNAME,
            user=self.settings.POSTGRES_USER,
            password=self.settings.POSTGRES_PASSWORD,
            host=self.settings.POSTGRES_HOST)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.conn:
                self.conn.commit()
        except Exception as exc:
            print(exc)
        finally:
            if self.conn:
                self.conn.close()
            if hasattr(self.conn, 'get_bind'):
                engine = self.conn.get_bind()
                engine.dispose()

    def execute(self, query):
        if self.cur:
            self.cur.execute(query)

    def add(self, _object: dataclass):
        if self.conn:
            self.conn.add(_object)