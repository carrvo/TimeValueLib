"""
Sets up package.
"""

from setuptools import setup, find_packages

setup(
    name='TimeValueLib',
    version='0.0',
    description='Economics Library representing the Time-Value property of money.',
    author='carrvo',
    author_email='carrvo@gmail.com',
    packages=find_packages(exclude=('tests',)),
    install_requires=[],
)
