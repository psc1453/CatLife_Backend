from abc import ABC, abstractmethod
from typing import Union

from lib.SQL.DB import DB


class DBTableProtocol(ABC):
    def __init__(self, db_instance: DB):
        self.db_instance = db_instance

    @property
    @abstractmethod
    def TABLE_NAME(self):
        pass

    @property
    @abstractmethod
    def EDITABLE_COLUMNS(self):
        pass

    @property
    @abstractmethod
    def PRIMARY_KEYS(self):
        pass

    @property
    @abstractmethod
    def FOREIGN_KEYS(self):
        pass

    @abstractmethod
    def insert_record(self, insert_dict: dict):
        pass

    @abstractmethod
    def fetch_record(self, for_key: Union[str, int]):
        pass

    @abstractmethod
    def delete_record(self, for_key: Union[str, int]):
        pass

    @abstractmethod
    def update_record(self, for_key: Union[str, int], new_dict: dict):
        pass
