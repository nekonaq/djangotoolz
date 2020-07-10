import os
from pyhiera import Hiera


def detect_settings_module(base_dir):
    envpath = os.path.realpath(os.path.join(base_dir, 'secrets/environment'))
    app_environ = os.path.basename(envpath) if os.path.exists(envpath) else 'local'
    return 'siteconf.settings.{}'.format(app_environ)


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
