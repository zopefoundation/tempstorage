Overview
========

A storage implementation which uses RAM to persist objects, much like
MappingStorage. Unlike MappingStorage, it needs not be packed to get rid of
non-cyclic garbage and it does rudimentary conflict resolution. This is a
ripoff of Jim's Packless bsddb3 storage.

**Please note: Usage of this package is deprecated, as it is known to randomly loose data, especially with zope 4.**

For details see: https://github.com/zopefoundation/tempstorage/issues/8
