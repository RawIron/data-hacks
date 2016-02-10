import sqlalchemy
from sqlalchemy.pool import NullPool
import psycopg2
from abc import ABCMeta, abstractmethod


class AlchemyEngine(object):
    __metaclass__ = ABCMeta

    @staticmethod
    def datetime_format():
        return "%Y-%m-%dT%H:%M:%S"

    @staticmethod
    def date_format():
        return "%Y-%m-%d"

    @abstractmethod
    def execute(self, sql):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def get_schema(self):
        pass


class AlchemyRedshiftEngine(AlchemyEngine):
    def __init__(self, settings):
        connect_info = """postgresql+psycopg2://%s:%s@%s:%s/%s""" % (
            settings['USER'],
            settings['PASSWORD'],
            settings['HOST'],
            settings['PORT'],
            settings['DB'],)

        engine = sqlalchemy.create_engine(connect_info, poolclass=NullPool)

        # allow access to alchemy engine and connection
        # this is required to use alchemy functions on the models
        # for example table.create(engine)
        self.engine = engine
        self.engine_type = 'redshift'
        self.conn = engine.connect()
        self.raw_conn = self.conn.connection

        self.schema = settings['SCHEMA']
        set_schema = """SET SEARCH_PATH TO %s""" % (settings['SCHEMA'])
        self.conn.execute(set_schema)

    def execute(self, sql, *args):
        # _must_ use raw connection
        # only on a raw connection the COPY command works
        cur = self.raw_conn.cursor()
        cur.execute(sql, *args)
        try:
            result = cur.fetchall()
        except psycopg2.ProgrammingError:
            result = []
        finally:
            self.raw_conn.commit()
        return result

    def close(self):
        self.conn.close()

    def get_schema(self):
        return self.schema


class AlchemyMysqlEngine(AlchemyEngine):
    def __init__(self, settings):
        connect_info = """mysql+mysqldb://%s:%s@%s:%s/%s?charset=utf8""" % (
            settings['USER'],
            settings['PASSWORD'],
            settings['HOST'],
            settings['PORT'],
            settings['DB'],)

        engine = sqlalchemy.create_engine(connect_info, encoding='utf-8', poolclass=NullPool)

        self.engine = engine
        self.engine_type = 'mysql'
        self.conn = engine.connect()

        self.schema = settings['DB']

    def execute(self, sql, *args):
        return self.conn.execute(sql, *args)

    def close(self):
        self.conn.close()

    def get_schema(self):
        return self.schema


def create_engine(settings):

    if settings['ENGINE'] == 'mysql':
        return AlchemyMysqlEngine(settings)

    elif settings['ENGINE'] == 'redshift':
        return AlchemyRedshiftEngine(settings)

    elif settings['ENGINE'] == 'postgres':
        return AlchemyRedshiftEngine(settings)
