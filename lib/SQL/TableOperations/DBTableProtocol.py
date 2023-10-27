from abc import ABC, abstractmethod

from ..DB import DB


class DBTableProtocol(ABC):
    def __init__(self, db_instance: DB):
        self.db_instance = db_instance

    @property
    @abstractmethod
    def table_name(self):
        pass

    @abstractmethod
    def insert_record(self, insert_dict: dict):
        pass

    @abstractmethod
    def fetch_record(self, for_key: str):
        pass

    @abstractmethod
    def delete_record(self, for_key: str):
        pass

    @abstractmethod
    def update_record(self, for_key: str, new_dict: dict):
        pass
