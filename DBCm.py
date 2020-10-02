import pyodbc


class ConnectionError(Exception):
    pass


class CredentialsError(Exception):
    pass


class SQLError(Exception):
    pass


class UseDatabase:

    def __init__(self, config: str) -> None:
        self.config = config

    def __enter__(self) -> 'Cursor':
        try:
            self.conn = pyodbc.connect(self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except pyodbc.DatabaseError as err:
            raise ConnectionError(err)
        except pyodbc.OperationalError as oerr:
            raise CredentialsError(oerr)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is pyodbc.ProgrammingError:
            raise SQLError(exc_val)
        elif exc_type:
            raise exc_type(exc_val)




