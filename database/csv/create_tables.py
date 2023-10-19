from pathlib import Path

import pandas as pd

from database.utils import load_yaml

tables_config_path = Path('../../tables.yml')
save_dir = Path('./tables')


def create_tables_dir_if_necessary(path):
    if not save_dir.exists():
        save_dir.mkdir()


if __name__ == '__main__':
    tables_config = load_yaml(tables_config_path)

    create_tables_dir_if_necessary(save_dir)

    for (table_name, table_content) in tables_config.items():
        column_labels = ([table_content['key']['label']] +
                         [column_attribute['label'] for (column_name, column_attribute) in
                          table_content['values'].items()])
        empty_data_frame = pd.DataFrame(data=None, columns=column_labels)
        file_name = table_content['file_name'] + '.csv'
        save_file = Path(file_name)
        save_path = Path(save_dir, save_file)
        empty_data_frame.to_csv(save_path, index=False)
