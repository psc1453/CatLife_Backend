import pandas as pd
import ruamel.yaml as yaml
from pathlib import Path

with open('tables.yml', 'r') as f:
    tables_config = yaml.safe_load(f)

save_dir = Path('./tables')
if not save_dir.exists():
    save_dir.mkdir()

for (table_name, table_content) in tables_config.items():
    column_labels = ([table_content['key']['label']] +
                     [column_attribute['label'] for (column_name, column_attribute) in table_content['values'].items()])
    empty_data_frame = pd.DataFrame(data=None, columns=column_labels)
    file_name = table_content['file_name'] + '.csv'
    save_file = Path(file_name)
    save_path = Path(save_dir, save_file)
    empty_data_frame.to_csv(save_path, index=False)
