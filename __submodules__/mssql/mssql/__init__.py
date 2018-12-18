import typing as t
from logging import Logger, getLogger

from .constants import DEFAULT_ALIAS
from .connection import connect, register


__version__ = "1.0"
__doc__ = "PyODBC wrappers for MS SQL Server connection."
__all__ = ['connect', 'register', 'BaseDBQuery']


class BaseDBQuery(object):
    def __init__(self, alias: str = DEFAULT_ALIAS, logger: Logger = None) -> None:
        self._conn = connect(alias)
        self.logger = logger if logger is not None else getLogger()

    def call(self, query: str, *params: t.Union[str, int]) -> t.Any:
        self.logger.debug(' '.join(query.replace('\n', '').strip().split()))
        return self._conn(query, *params)

    def to_dict(self, row: t.Any) -> dict:
        """ Конвертирует запись, возвращаемую курсором PyODBC в словарь. """
        return self._conn.to_dict(row)
