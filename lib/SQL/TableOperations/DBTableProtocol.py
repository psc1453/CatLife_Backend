from abc import ABC, abstractmethod

from ..DB import DB


class DBTableProtocol(ABC):
    def __init__(self, db_instance: DB, table_name: str):
        self.db_instance = db_instance
        self.table_name = table_name

    @abstractmethod
    def insert_record(self, insert_dict: dict):
        pass

    @abstractmethod
    def fetch_table(self, option: str):
        pass
