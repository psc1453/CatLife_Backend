from pathlib import Path

import pandas as pd

from database.utils import load_yaml


def create_tables_dir_if_necessary(path):
    path = Path(path)
    if not path.exists():
        path.mkdir()


def create_tables(yaml_path, save_dir):
    tables_config = load_yaml(yaml_path)

    create_tables_dir_if_necessary(save_dir)

    for (table_name, table_content) in tables_config.items():
        column_labels = ([table_content['key']['label']] +
                         [column_attribute['label'] for (column_name, column_attribute) in
                          table_content['values'].items()])
        empty_data_frame = pd.DataFrame(data=None, columns=column_labels)
        file_name = table_content['file_name'] + '.csv'
        save_file = Path(file_name)
        save_path = Path(save_dir, save_file)
        if not save_path.exists():
            empty_data_frame.to_csv(save_path, index=False)
