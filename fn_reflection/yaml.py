import yaml


def safe_load(filepath: str):
    with open(filepath) as yml:
        res = yaml.safe_load(yml)
    return res
