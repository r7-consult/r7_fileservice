import logging
from datetime import datetime as date_time
from sqlite3 import connect
from xldb_config import SETTINGS


class DatabaseHandler(logging.Handler):
    def __init__(self, db_file):
        super().__init__()
        self.db_file = db_file
        self.db_file = connect(self.db_file, check_same_thread=False)
        self.db_file.execute('CREATE TABLE IF NOT EXISTS logs ('
                             'date TEXT, time TEXT, lvl INTEGER, lvl_name TEXT, msg TEXT, '
                             'logger TEXT, lineno INTEGER)')

    def emit(self, record):
        self.db_file.execute(
                    'INSERT INTO logs VALUES (:1,:2,:3,:4,:5,:6,:7)', (
                        date_time.now().strftime('%A, the %d of %B, %Y'),
                        date_time.now().strftime('%I:%M %p'),
                        int(record.levelno),
                        record.levelname,
                        str(record.msg),
                        record.name,
                        record.lineno
                        )
                )
        self.db_file.commit()


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger_formatter = logging.Formatter(
    fmt='%(levelno)s %(levelname)s, %(name)s - "%(message)s at %(asctime)s"',
    datefmt='%Y-%m-%d %H:%M:%S'  # datefmt='%I:%M %p on %A, the %d of %B, %Y'
)

logger_stream_handler = logging.StreamHandler()
logger_stream_handler.setFormatter(logger_formatter)
logger_stream_handler.setLevel(logging.DEBUG)
logger_database_handler = DatabaseHandler(SETTINGS.xldb_loger_db)
logger_database_handler.setLevel(logging.DEBUG)
logger.addHandler(logger_stream_handler)
logger.addHandler(logger_database_handler)
