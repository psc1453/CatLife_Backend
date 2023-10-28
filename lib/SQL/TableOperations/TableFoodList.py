from lib.SQL.DB import DB
from lib.SQL.TableOperations.DBTableProtocol import DBTableProtocol


class TableFoodList(DBTableProtocol):
    def __init__(self, db_instance: DB):
        super().__init__(db_instance)

    @property
    def TABLE_NAME(self):
        return 'FoodList'

    @property
    def EDITABLE_COLUMNS(self):
        return ['food_brand', 'food_name', 'food_category', 'food_unit']

    def insert_record(self, insert_dict: dict):
        assert all((key in self.EDITABLE_COLUMNS) for key in list(
            insert_dict.keys())), \
            'Find unsupported keys, only [food_brand, food_name, food_category, food_unit] are supported'

        self.db_instance.insert_table_by_dict(self.TABLE_NAME, insert_dict)

    def fetch_record(self, for_key: int):
        command = f'''
            SELECT *
            FROM {self.TABLE_NAME}
            WHERE food_id = {for_key}
        '''
        table = self.db_instance.fetch_table_by_command(command)
        return table

    # TODO: Add the delete and update functions.
    def delete_record(self, for_key: int):
        pass

    def update_record(self, for_key: int, new_dict: dict):
        pass

    def add_food_record(self, brand: str, name: str, category: str, unit: str):
        self.insert_record({'food_brand': brand,
                            'food_name': name,
                            'food_category': category,
                            'food_unit': unit})

    def get_food_record_by_id(self, food_id: int):
        return self.fetch_record(food_id)

    def find_food_record_by_name(self, name: str):
        command = f'''
            SELECT *
            FROM {self.TABLE_NAME}
             WHERE food_name LIKE \'%{name}%\'
        '''
        return self.db_instance.fetch_table_by_command(command)

    def get_food_list(self):
        command = f'''
            SELECT *
            FROM {self.TABLE_NAME}
        '''
        return self.db_instance.fetch_table_by_command(command)

    def get_food_product_list(self):
        command = f'''
            SELECT CONCAT_WS('-', food_brand, food_name) AS product_name
            FROM {self.TABLE_NAME}
        '''
        return self.db_instance.fetch_table_by_command(command)


def test():
    db = DB.from_yaml('../../../db_info.yml')
    table_food = TableFoodList(db)

    table_food.insert_record({'food_brand': '百事', 'food_name': '可乐', 'food_category': '饮料', 'food_unit': '罐'})

    result = table_food.get_food_record_by_id(15)
    print(result)
    search = table_food.find_food_record_by_name('猫条')
    print(search)
    all = table_food.get_food_list()
    print(all)
    products = table_food.get_food_product_list()
    print(products)


if __name__ == '__main__':
    test()
