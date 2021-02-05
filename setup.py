# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join

try:
    from setuptools import setup
except ImportError as error:
    from distutils.core import setup


version_file = join(dirname(abspath(__file__)), 'Mainframe3270', 'version.py')

with open(version_file) as file:
    code = compile(file.read(), version_file, 'exec')
    exec(code)

setup(name             = 'robotframework-mainframe3270',
      version          = '2.10',
      description      = 'Mainframe Test library for Robot Framework',
      long_description = 'Test library for Robot Framework to enable to create automated test scripts to test IBM Mainframe 3270',
      author           = 'Altran Portugal',
      author_email     = 'samuel.cabral@altran.com',
      license          = 'MIT License',
      url              = 'https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library',
      packages         = ['Mainframe3270'],
      install_requires = ['robotframework', 'six']
      )
