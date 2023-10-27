from abc import ABC, abstractmethod


class DBTableProtocol(ABC):
    def __init__(self, table_name):
        self.table_name = table_name

    @abstractmethod
    def insert_record(self, insert_dict):
        pass

    @abstractmethod
    def fetch_table(self, option):
        pass
