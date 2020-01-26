import importlib


def import_module_from_path(path):
    module_name = path.split('.')[0].replace('/', '.')
    module = importlib.import_module(module_name)
    return module