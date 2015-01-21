# try:
from setuptools import setup, find_packages 
# except ImportError:
#     from distutils.core import setup

setup(
    name='svven-aggregator',
    version='0.1',
    author='Alexandru Stanciu',
    author_email='ducu@svven.com',
    packages=find_packages(),
    include_package_data = True,
    url='https://bitbucket.org/svven/aggregator',
    description='Aggregator models and helpers working with Redis.',
    install_requires=[
        'Jinja2>=2.7.3',
        'redis>=2.9.1',
        'svven-database>=0.1',
    ],
)