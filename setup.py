#!/usr/bin/env python
from os.path import dirname, join, abspath
from setuptools import setup, find_packages

here = dirname(abspath(__file__))
readme = join(here, "README.rst")

setup(
    name='fit',
    version='0.4.1',
    packages=find_packages(),
    url='https://github.com/rembish/fit',
    license='BSD',
    author='Aleksey Rembish',
    author_email='alex@rembish.org',
    description='FIT file I/O',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
    ],
    long_description=open(readme).read())
