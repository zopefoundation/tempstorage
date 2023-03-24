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

from setuptools import find_packages
from setuptools import setup


long_description = (open("README.rst").read() + "\n" +
                    open("CHANGES.rst").read())
version = '6.0'
__version__ = version


setup(name='tempstorage',
      version=__version__,
      url='https://github.com/zopefoundation/tempstorage',
      project_urls={
        'Issue Tracker': ('https://github.com/zopefoundation/'
                          'tempstorage/issues'),
        'Sources': 'https://github.com/zopefoundation/tempstorage',
      },
      license='ZPL 2.1',
      description='A RAM-based storage for ZODB',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.dev',
      long_description=long_description,
      classifiers=[
          "Development Status :: 6 - Mature",
          "Environment :: Web Environment",
          "Framework :: ZODB",
          "Framework :: Zope",
          "Framework :: Zope :: 4",
          "Framework :: Zope :: 5",
          "Intended Audience :: Developers",
          "License :: OSI Approved",
          "License :: OSI Approved :: Zope Public License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Internet",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: Session",
      ],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      python_requires='>=3.7',
      install_requires=[
          'setuptools',
          'ZODB >= 5.6',
          'zope.testing',
      ],
      extras_require={
          'test': [
              'zope.testrunner',
              'mock ; python_version < "3"',
          ],
      },
      include_package_data=True,
      zip_safe=False,
      keywords=['zope', 'plone', 'zodb']
      )
