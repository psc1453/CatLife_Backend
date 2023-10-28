from abc import ABC, abstractmethod
from typing import Union

from ..DB import DB


class DBTableProtocol(ABC):
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
    def fetch_record(self, for_key: Union[str, int]):
        pass
