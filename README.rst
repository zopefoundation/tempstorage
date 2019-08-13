Overview
========

A storage implementation which uses RAM to persist objects, much like
MappingStorage. Unlike MappingStorage, it needs not be packed to get rid of
non-cyclic garbage and it does rudimentary conflict resolution. This is a
ripoff of Jim's Packless bsddb3 storage.

**Please note: Usage of this package is deprecated, as it is known to randomly loose data, especially with Zope 4.**

For a detailed discussion see `#8 <https://github.com/zopefoundation/tempstorage/issues/8>`_ as well as `#12 <https://github.com/zopefoundation/tempstorage/issues/12>`_

To replace server-side sessions, cookies are probably your best bet, as these also get rid of any denial of service problems that server side sessions are vulnerable to.

If you need server side storage of sessions, consider using a normal store rather than tempstorage for your session data.
For details and suggestions see `this discussion in the pull request <https://github.com/zopefoundation/tempstorage/pull/14#issuecomment-520318459>`_ as well as the discussion in the aforementioned bug reports as well as `the discussion in Zope about the removal of the generated configuration <https://github.com/zopefoundation/Zope/pull/684>`_.
