import os
import sys

from setuptools import find_packages, setup

NAME = "benchmark"
DESCRIPTION = 'Modern sparse linear regression'
URL = 'https://github.com/ohjeah/regression-benchmark'
EMAIL = 'info@markusqua.de'
AUTHOR = 'Markus Quade'

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "requirements.txt"), "r") as f:
    REQUIRED = f.readlines()

about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=__doc__,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=["test", "example"]),
    install_requires=REQUIRED,
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
