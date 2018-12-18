import typing as t
import pyodbc

from .constants import DEFAULT_ALIAS, DEFAULT_PORT

__all__ = ['connect', 'register', 'MsSQLClient']

_connections = {}
T = t.TypeVar('T', bound='MsSQLClient')


def register(alias: str, mock_class: type = None, **kwargs) -> t.Any:
    _connections[alias] = mock_class(**kwargs) if mock_class is not None else MsSQLClient(**kwargs)
    return _connections[alias]


def connect(alias: str = DEFAULT_ALIAS, **kwargs) -> t.Any:
    return _connections[alias] if alias in _connections else register(alias, **kwargs)


class MsSQLClient(object):
    def __init__(self, server: str, database: str, user: str, password: str,
                 port: int = DEFAULT_PORT, autoconnect: bool = True) -> None:
        self.settings = {'server': server, 'database': database, 'user': user, 'password': password, 'port': port}
        self.connect() if autoconnect else None

    def cursor(self) -> pyodbc.Cursor:
        try:
            return self._conn.cursor()
        except pyodbc.ProgrammingError:
            return self.connect().cursor()

    def connect(self: T) -> T:
        self._conn = pyodbc.connect(
            'DRIVER={{FreeTDS}};SERVER={server};PORT={port};DATABASE={database};UID={user};PWD={password};'
            'TDS_Version=8.0;ClientCharset=UTF8;'.format(**self.settings),
            autocommit=True
        )
        return self

    def disconnect(self: T) -> T:
        try:
            self._conn.close()
        except pyodbc.ProgrammingError:
            pass
        return self

    def to_dict(self, row: pyodbc.Cursor) -> dict:
        """ Конвертирует запись, возвращаемую курсором PyODBC в словарь. """
        return {column: row[i] for i, column in enumerate([param[0].lower() for param in row.cursor_description])}

    def __call__(self, query: str, *params: t.Union[str, int]) -> pyodbc.Cursor:
        return self.cursor().execute(query, *params)
