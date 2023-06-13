from setuptools import setup, find_packages

setup(
    name="bookr",
    version='0.0.1',
    packages=find_packages(include=['utils', 'models', 'controllers', 'routes', 'tests'])
)