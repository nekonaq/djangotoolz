#!/usr/bin/env python3
from setuptools import setup, find_namespace_packages

import re
import os

version = re.search("__version__ = '([^']+)'", open(
    os.path.join(os.path.dirname(__file__), 'djangoexpack/version.py')
).read().strip()).group(1)

setup(
    name='djangoexpack',
    version=version,
    author="Tatsuo Nakajyo",
    author_email="tnak@nekonaq.com",
    license='BSD',

    zip_safe=False,
    packages=find_namespace_packages(include=['djangoexpack.*']),
    # include_package_data=True,

    python_requires='~=3.6.9',
    # install_requires=['pyhiera'],
)

# Local Variables:
# compile-command: "python3 ./setup.py sdist"
# End:
