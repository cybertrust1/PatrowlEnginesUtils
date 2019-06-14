#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup file."""


from setuptools import setup, find_packages

setup(
    name='PatrowlEnginesUtils',
    version='0.0.8',
    description='Common classes for PatrowlEngines',
    url='https://github.com/Patrowl/PatrowlEnginesUtils',
    author='Nicolas Mattiocco',
    author_email='getsupport@patrowl.io',
    license='AGPLv3',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
