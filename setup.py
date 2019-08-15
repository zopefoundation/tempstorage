##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""Setup for the tempstorage package
"""

from setuptools import setup, find_packages

long_description = (open("README.rst").read() + "\n" +
                    open("CHANGES.rst").read())

version = '5.1'
__version__ = version

setup(name='tempstorage',
      version=__version__,
      url='https://github.com/zopefoundation/tempstorage',
      license='ZPL 2.1',
      description='A RAM-based storage for ZODB',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      long_description=long_description,
      classifiers=[
          "Development Status :: 7 - Inactive",
          "Environment :: Web Environment",
          "Framework :: ZODB",
          "Framework :: Zope",
          "Framework :: Zope :: 4",
          "Intended Audience :: Developers",
          "License :: OSI Approved",
          "License :: OSI Approved :: Zope Public License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Internet",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: Session",
      ],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=[
          'setuptools',
          'ZODB >= 5.0',
          'zope.testing',
      ],
      extras_require={
          'test': [
              'mock',
              'zope.testrunner'
          ],
      },
      include_package_data=True,
      zip_safe=False,
      keywords=['zope', 'plone', 'zodb']
      )
