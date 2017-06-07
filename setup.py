from setuptools import setup, find_packages

requires = ["numpy", "toolz", "pyodesys"]

setup(
    name="regression_benchmark",
    version="0.0.1",
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
)
