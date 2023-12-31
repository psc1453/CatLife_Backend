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

    @property
    def PRIMARY_KEY(self):
        return 'food_id'

    @property
    def FOREIGN_KEYS(self):
        return []

    def add_food_record(self, brand: str, name: str, category: str, unit: str):
        self.insert_record({'food_brand': brand,
                            'food_name': name,
                            'food_category': category,
                            'food_unit': unit})

    def get_food_records_all(self):
        return self.fetch_table()

    def get_food_products_all(self):
        command = f'''
            SELECT food_id, CONCAT_WS('-', food_brand, food_name) AS product_name
            FROM {self.TABLE_NAME}
        '''
        return self.db_instance.fetch_table_by_command(command)

    def get_food_record_by_id(self, food_id: int):
        return self.fetch_record(food_id)

    def find_food_records_by_name(self, name: str):
        command = f'''
            SELECT *
            FROM {self.TABLE_NAME}
             WHERE food_name LIKE \'%{name}%\'
        '''
        return self.db_instance.fetch_table_by_command(command)

    def delete_food_record_by_id(self, food_id: int):
        self.delete_record(food_id)

    def update_food_record_by_id_with_dict(self, food_id: int, update_dict: dict):
        self.update_record(food_id, update_dict)


def test():
    db = DB.from_yaml('../../../db_info.yml')
    table_food = TableFoodList(db)

    table_food.insert_record({'food_brand': '百事', 'food_name': '可乐', 'food_category': '饮料', 'food_unit': '罐'})

    result = table_food.get_food_record_by_id(15)
    print(result)
    search = table_food.find_food_records_by_name('猫条')
    print(search)
    all = table_food.get_food_records_all()
    print(all)
    products = table_food.get_food_products_all()
    print(products)


if __name__ == '__main__':
    test()
