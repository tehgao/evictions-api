#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='evictions_api',
      version='1.0',
      packages=find_packages(),
      scripts=['manage.py'],
      install_requires=[
          'django',
          'djangorestframework',
          'pdfmajor',
      ])
