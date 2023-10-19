import ruamel.yaml as yaml


def load_yaml(path):
    with open(path, 'r') as f:
        yaml_dict = yaml.safe_load(f)
        return yaml_dict
