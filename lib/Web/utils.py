def table_to_dict(table: list[tuple]):
    column_names, records = table[0], table[1:]
    column_names_list = list(column_names)
    records_list = [list(record) for record in records]
    dict_data = {
        'column_names': column_names_list,
        'records': records_list
    }
    return dict_data


def test():
    example = [('n1', 'n2'), ('v1', 'v2'), ('v3', 'v4')]
    result = table_to_dict(example)
    print(result)


if __name__ == '__main__':
    test()
