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
    def PRIMARY_KEY(self):
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

    def delete_record(self, for_key: Union[str, int]):
        self.db_instance.delete_row_from_table_by_key(self.TABLE_NAME, self.PRIMARY_KEY, for_key)

    def update_record(self, for_key: Union[str, int], update_dict: dict):
        self.db_instance.update_row_in_table_by_key_with_dict(self.TABLE_NAME, self.PRIMARY_KEY, for_key, update_dict)
