import importlib
module = importlib.import_module('fbs_runtime._frozen')
module.BUILD_SETTINGS = {'app_name': 'panel_builder', 'author': 'John Vorsten', 'version': '0.0.1', 'environment': 'production'}