import os
from pyhiera import Hiera


def load_settings_from_config(hiera_configs, **context):
    for confpath in hiera_configs if isinstance(hiera_configs, (list, tuple)) else (hiera_configs,):
        if not os.path.exists(confpath):
            continue
        print("# config:", confpath)
        hiera = Hiera.load_data(confpath, context=context)
        hiera_data = hiera.flatten()
        return hiera_data

    print("# WARNING -- no config file found.")
    return {}
