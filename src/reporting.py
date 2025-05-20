import logging
from time import time
from pydantic import BaseModel
from typing import List, Tuple

logger = logging.getLogger(__name__)

SQL_RESPONSE = {
    'meta': [],
    'data': [],
    'rows': 0,
    'rows_before_limit_at_least': 1,
    'statistics': {
        'elapsed': '',
        'rows_read': 0,
        'bytes_read': 0
    }
}


class QueryStatistics(BaseModel):
    elapsed: int = 0
    rows_read: int = 0
    bytes_read: int = 0


class QueryColumnsMeta(BaseModel):
    name: str = ''
    type: str = ''


class QueryStatReport(BaseModel):
    meta: List[QueryColumnsMeta] = []
    data: List = []
    rows: int = 0
    rows_before_limit_at_least: int = 1
    statistics: QueryStatistics = QueryStatistics()
    error: str = ''
    connection: str = ''


class QueryResponseStatistics:
    def __init__(self):
        self.start_time = time()
        self.report = QueryStatReport()
        self.column_types_map = {}

    def query_info(self, sql, metadata, error):
        NAME_INDEX = 0
        TYPE_INDEX = 1
        self.report.meta = [{'name': column_info[NAME_INDEX],
                             'type': self.column_types_map.get(column_info[TYPE_INDEX], str(column_info[TYPE_INDEX]))}
                             for column_info in metadata]
        self.report.statistics.bytes_read = 0
        self.report.statistics.elapsed = f'{(time() - self.start_time):.4f} sec'
        self.report.error = str(error),
        self.connection(sql)
        logger.debug(f'self.report={self.report}')

    def query_data(self, data):
        self.report.data = data

    def query_rows(self, rows):
        self.report.rows = rows

    def query_len(self, data_len):
        self.report.statistics.rows_read = data_len

    def query_bytes(self, data_bytes):
        self.report.statistics.bytes_read = data_bytes

    def connection(self, sql: SQL_RESPONSE):
        self.report.connection = (f'dbms_host={sql.dbms_host}, '
                                  f'dbms_port={sql.dbms_port}, '
                                  #f'user={sql.user}, '
                                  #f'password={sql.password}, '
                                  f'database={sql.database},'
                                  f'sid={sql.sid}, '
                                  f'query={sql.query}')
