Changelog
=========

6.0 (2023-03-24)
----------------


- Add support for Python 3.10, 3.11.

- Drop support for Python 2.7, 3.5, 3.6.

5.2 (2021-07-05)
----------------

- Update package configuration

- Package is now officially undeprecated because the data corruption issue -
  that was the reason for its deprecation - has been understood and fixed. See
  (`#16 <https://github.com/zopefoundation/tempstorage/issues/16>`_).

- Add support for Python 3.8 and Python 3.9.


5.1 (2019-08-15)
----------------

- Package is now officially deprecated as it was broken for many years. This 
  was/ is common knowledge in the zope community, but was not documented 
  anywhere and thus this package was still used by many community members 
  without knowing this. See
  (`#8 <https://github.com/zopefoundation/tempstorage/issues/8>`_)
  (`#12 <https://github.com/zopefoundation/tempstorage/issues/12>`_)


5.0 (2019-05-10)
----------------

- Update PyPy version.

- Drop Python 3.4 support.

- Add support for Python 3.7.

- Avoid RuntimeError in _takeOutGarbage. See `issue 7
  <https://github.com/zopefoundation/tempstorage/issues/7>`_.


4.0.1 (2017-11-27)
------------------
- Raise POSKeyError instead of KeyError in loadBefore.


4.0 - 2017-03-09
----------------

- Drop Python 3.3 compatibility, add Python 3.6 compatibility.

- Require ZODB 5.0 or newer.

- Use `storage._lock` as a context manager.

- Declare PyPy compatibility.


3.0 - 2016-04-03
----------------

- Python 3.3-3.5 compatibility.


2.12.2 - 2012-10-14
-------------------

- Explicitly state distribution dependencies instead of re-using the
  ZODB test requirements.

2.12.1 - 2010-09-29
-------------------

- Disabled ``check_tid_ordering_w_commit`` test from BasicStorage, as it uses
  invalid test data.


2.12.0 - 2010-09-25
-------------------

- Require at least ZODB 3.9 and adjusted method signatures to disuse versions.

- Expanded dependency on ZODB3 to include the test extra.


2.11.3 - 2010-06-05
-------------------

- Approximate PEP8 compliance.

- Split out the ZODB protocol tests from the tests specific to the module.
  Make the local tests use "normal" unittest conventions.

- Comply with repository policy.

- Clean imports, docstrings;  add an instance-level hook for GC parms.

- Fix a test failure due to never-unghostified root in second connection.


2.11.2 - 2009-08-03
-------------------

- Added change log and readme.

- Lauchpad #143736, #271395: fixed AttributeError' on _ltid in TempStorage


2.11.1 - 2008-08-05
-------------------

- Initial release as a stand-alone package.
