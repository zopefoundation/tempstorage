##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Setup for the Acquisition egg package
"""
import os
from setuptools import setup, find_packages, Extension

setup(name='tempstorage',
      version = '2.11.0b1',
      url='http://pypi.python.org/pypi/tempstorage',
      license='ZPL 2.1',
      description='A RAM-based storage for ZODB',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      long_description="""\
A storage implementation which uses RAM to persist objects, much like
MappingStorage.  Unlike MappingStorage, it needs not be packed to get rid of
non-cyclic garbage and it does rudimentary conflict resolution.  This is a
ripoff of Jim's Packless bsddb3 storage.""",
      
      packages=find_packages('src'),
      package_dir={'': 'src'},

      install_requires=['ZODB3'],
      include_package_data=True,
      zip_safe=False,
      )
