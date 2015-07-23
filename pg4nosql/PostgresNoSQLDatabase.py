import psycopg2
from psycopg2.extensions import AsIs
from pg4nosql import DEFAULT_POSTGRES_DATABASE
from pg4nosql.PostgresNoSQLTable import PostgresNoSQLTable


class PostgresNoSQLDatabase(object):
    __SQL_CREATE_JSON_TABLE = 'CREATE TABLE %s (id SERIAL %s, data JSON);'
    __SQL_DROP_JSON_TABLE = 'DROP TABLE IF EXISTS %s;'
    __SQL_TABLE_EXISTS = "SELECT EXISTS(SELECT relname FROM pg_class WHERE relname=%s)"

    def __init__(self, name, host, user, password):
        self.name = name
        self.connection = psycopg2.connect(host=host, database=name, user=user, password=password)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def commit(self):
        self.connection.commit()

    def create_table(self, table_name, relational_columns={}):
        # create additional columns string
        columns_str = ''.join(', %s %s' % (key, val) for (key, val) in relational_columns.iteritems())
        self.cursor.execute(self.__SQL_CREATE_JSON_TABLE, (AsIs(table_name), AsIs(columns_str)))
        self.commit()
        return PostgresNoSQLTable(table_name, self.connection)

    def drop_table(self, table_name):
        self.cursor.execute(self.__SQL_DROP_JSON_TABLE, (AsIs(table_name),))
        self.commit()

    def get_table(self, table_name):
        if self.table_exists(table_name):
            return PostgresNoSQLTable(table_name, self.connection)
        else:
            return None

    def get_or_create_(self, table_name):
        table = self.get_table(table_name)
        if not table:
            table = self.create_table(table_name)
        return table

    def table_exists(self, table_name):
        exists = False
        try:
            self.cursor.execute(self.__SQL_TABLE_EXISTS, (table_name,))
            exists = self.cursor.fetchone()[0]
        except psycopg2.Error as e:
            print e
        return exists