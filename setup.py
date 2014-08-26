#!/usr/bin/env python
"""
The Flexible and Interoperable Data Transfer (FIT) protocol is a format designed
specifically for the storing and sharing of data that originates from sport,
fitness and health devices. It is specifically designed to be compact,
interoperable and extensible. This document will describe the FIT file structure
and interpretation.

The FIT protocol defines a set of data storage templates (FIT messages) that can
be used to store information such as user profiles and activity data in files.
Any FIT-compliant device can interpret a FIT file from any other FIT-compliant
device.

This library provides unified access to any valid FIT file. You can read,
update and than write back your FIT files.
"""
from setuptools import setup, find_packages

setup(
    name='fit',
    version='0.4.0',
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
    long_description=__doc__)
