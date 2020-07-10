import os
import yaml
from importlib import import_module


def load_config(base_dir):
    """呼び出し側の settings 名前空間を設定ファイルの内容でアップデートする
    """
    settings_file = os.path.join(base_dir, 'config', 'settings.yml')
    settings_dict = None
    try:
        with open(settings_file, 'r') as fp:
            settings_dict = yaml.safe_load(fp)
    except FileNotFoundError:
        pass

    return settings_dict or {}


def get_module_dir(name):
    """モジュールのディレクトリを取得する
    """
    mod = import_module(name)
    return os.path.dirname(mod.__file__)
