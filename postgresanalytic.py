from psycopg2 import sql
import psycopg2

DB_NAME_POSTGRES = "test1"
DB_USER_POSTGRES = "postgres"
DB_PASSWORD_POSTGRES = "mysecretpassword"
DB_HOST_POSTGRES = "localhost"
DB_PORT_POSTGRES = "5432"

import psycopg2


class Postgrespipeline:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(
        self, host=None, port=None, username=None, password=None, database=None
    ) -> None:
        if hasattr(self, "__initialized") and self.__initialized:
            return
        self.__initialized = True
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def _connect(self):
        return psycopg2.connect(
            database=self.database,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
        )

    def execute_query(self, query):
        try:
            with self._connect() as client:
                with client.cursor() as cursor:
                    cursor.execute(query)
                    if cursor.description:
                        result = cursor.fetchall()
                    else:
                        result = None
            return True, result
        except Exception as e:
            print("error",e)
            return False, e
