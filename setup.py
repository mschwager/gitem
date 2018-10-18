from setuptools import (
    find_packages,
    setup,
)

import os
import sys

PACKAGE_DIRECTORY = 'lib'

sys.path.append(PACKAGE_DIRECTORY)

import gitem

requirements_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')

with open(requirements_filename) as fd:
    install_requires = [i.strip() for i in fd.readlines()]

requirements_dev_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'requirements-dev.txt')

with open(requirements_dev_filename) as fd:
    tests_require = [i.strip() for i in fd.readlines()]

long_description_filename = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'README.md')

with open(long_description_filename) as fd:
    long_description = fd.read()

setup(
    name=gitem.__name__,
    version=gitem.__version__,
    description='A Github organization reconnaissance tool.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mschwager/gitem',
    packages=find_packages(where=PACKAGE_DIRECTORY),
    package_dir={'': PACKAGE_DIRECTORY},
    license='GPLv3',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            'gitem = gitem.__main__:main',
        ],
    },
)
