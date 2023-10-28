from abc import ABC, abstractmethod
from typing import Union

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
    def fetch_record(self, for_key: Union[str, int]):
        pass

    @abstractmethod
    def delete_record(self, for_key: Union[str, int]):
        pass

    @abstractmethod
    def update_record(self, for_key: Union[str, int], new_dict: dict):
        pass
