from abc import ABC, abstractmethod

from lib.SQL.DB import DB


class DBViewProtocol(ABC):
    def __init__(self, db_instance: DB):
        self.db_instance = db_instance

    @property
    @abstractmethod
    def VIEW_NAME(self):
        pass

    @property
    @abstractmethod
    def READABLE_COLUMNS(self):
        pass

    @abstractmethod
    def fetch_record(self, for_key: str):
        pass
