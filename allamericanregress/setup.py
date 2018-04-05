#!/usr/bin/env python3
"""Setup script for installing the allamericanregress package.
Install with `python setup.py install`."""
import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    # TODO: Use frozen path
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# print(read('requirements.txt').split('\n'))
setup(
    name='allamericanregress',
    version=0.1,
    description='Capstone project.',
    # long_description=read('README'),
    url='https://github.com/jcrayz/Capstone',
    author='AllAmericanRegress',
    author_email='',
    include_package_data=True,
    setup_requires=[],
)
