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

import unittest

from ZODB.tests import BasicStorage
from ZODB.tests import ConflictResolution
from ZODB.tests import MTStorage
from ZODB.tests import StorageTestBase
from ZODB.tests import Synchronization
from ZODB.utils import p64
from ZODB.utils import u64


def handle_all_serials(oid, *args):
    """Return dict of oid to serialno from store() and tpc_vote().

    Raises an exception if one of the calls raised an exception.

    The storage interface got complicated when ZEO was introduced.
    Any individual store() call can return None or a sequence of
    2-tuples where the 2-tuple is either oid, serialno or an
    exception to be raised by the client.

    The original interface just returned the serialno for the
    object.

    The updated multi-commit API returns nothing from store(), and
    returns a sequence of resolved oids from tpc_vote.

    NOTE: This function is removed entirely in ZODB 5.
    """
    d = {}
    for arg in args:
        if isinstance(arg, bytes):
            d[oid] = arg
        elif arg:
            for t in arg:
                if isinstance(t, bytes):
                    # New protocol. The caller will use the tid
                    # returned from tpc_finish if we return a dict
                    # missing the oid.
                    pass
                else:
                    oid, serial = t
                    if not isinstance(serial, bytes):
                        raise serial  # error from ZEO server
                    d[oid] = serial
    return d


def handle_serials(oid, *args):
    """Return the serialno for oid based on multiple return values.

    A helper for function _handle_all_serials().
    """
    return handle_all_serials(oid, *args).get(oid)


class ZODBProtocolTests(StorageTestBase.StorageTestBase,
                        BasicStorage.BasicStorage,
                        Synchronization.SynchronizedStorage,
                        ConflictResolution.ConflictResolvingStorage,
                        MTStorage.MTStorage):

    def setUp(self):
        StorageTestBase.StorageTestBase.setUp(self)
        self.open()

    def open(self, **kwargs):
        from tempstorage.TemporaryStorage import TemporaryStorage
        self._storage = TemporaryStorage('foo')

    def test_tid_ordering_w_commit(self):
        # The test uses invalid test data of 'x'. The normal storages
        # don't load the actual data and thus pass, but the tempstorage
        # will always try to load the data and fail
        pass


class TemporaryStorageTests(unittest.TestCase):

    def _getTargetClass(self):
        from tempstorage.TemporaryStorage import TemporaryStorage
        return TemporaryStorage

    def _makeOne(self, name='foo'):
        return self._getTargetClass()(name)

    def _dostore(self, storage, oid=None, revid=None, data=None,
                 already_pickled=0, user=None, description=None):
        # Borrowed from StorageTestBase, to allow passing storage.
        """Do a complete storage transaction.  The defaults are:

         - oid=None, ask the storage for a new oid
         - revid=None, use a revid of ZERO
         - data=None, pickle up some arbitrary data (the integer 7)

        Returns the object's new revision id.
        """
        from ZODB.Connection import TransactionMetaData
        from ZODB.tests.MinPO import MinPO

        if oid is None:
            oid = storage.new_oid()
        if revid is None:
            revid = StorageTestBase.ZERO
        if data is None:
            data = MinPO(7)
        if type(data) == int:
            data = MinPO(data)
        if not already_pickled:
            data = StorageTestBase.zodb_pickle(data)
        # Begin the transaction
        t = TransactionMetaData()
        if user is not None:
            t.user = user
        if description is not None:
            t.description = description
        try:
            storage.tpc_begin(t)
            # Store an object
            r1 = storage.store(oid, revid, data, '', t)
            # Finish the transaction
            r2 = storage.tpc_vote(t)
            revid = handle_serials(oid, r1, r2)
            storage.tpc_finish(t)
        except:  # noqa: E722 bare except
            storage.tpc_abort(t)
            raise
        return revid

    def _do_read_conflict(self, db, mvcc):
        import transaction
        from ZODB.tests.MinPO import MinPO
        tm1 = transaction.TransactionManager()
        conn = db.open(transaction_manager=tm1)
        r1 = conn.root()
        obj = MinPO('root')
        r1["p"] = obj
        obj = r1["p"]
        obj.child1 = MinPO('child1')
        tm1.get().commit()

        # start a new transaction with a new connection
        tm2 = transaction.TransactionManager()
        cn2 = db.open(transaction_manager=tm2)
        r2 = cn2.root()
        r2["p"]._p_activate()

        self.assertEqual(r1._p_serial, r2._p_serial)

        obj.child2 = MinPO('child2')
        tm1.get().commit()

        # resume the transaction using cn2
        obj = r2["p"]

        # An attempt to access obj.child1 should fail with an RCE
        # below if conn isn't using mvcc, because r2 was read earlier
        # in the transaction and obj was modified by the other
        # transaction.

        obj.child1
        return obj

    def test_conflict_cache_clears_over_time(self):
        import time

        from ZODB.tests.MinPO import MinPO
        storage = self._makeOne()
        storage._conflict_cache_gcevery = 1  # second
        storage._conflict_cache_maxage = 1  # second

        # assertCacheKeys asserts that
        # set(storage._conflict_cache.keys()) == oidrevSet
        # storage._conflict_cache is organized as {} (oid,rev) -> (data,t) and
        # so is used by loadBefore as data storage. It is important that latest
        # revision of an object is not garbage-collected so that loadBefore
        # does not loose what was last committed.
        def assertCacheKeys(*voidrevOK):
            oidrevOK = set(voidrevOK)
            self.assertEqual(set(storage._conflict_cache.keys()), oidrevOK)
            # make sure that loadBefore actually uses ._conflict_cache data
            for (oid, rev) in voidrevOK:
                load_data, load_serial, _ = storage.loadBefore(oid,
                                                               p64(u64(rev)+1))
                data, t = storage._conflict_cache[(oid, rev)]
                self.assertEqual((load_data, load_serial), (data, rev))

        oid1 = storage.new_oid()
        self._dostore(storage, oid1, data=MinPO(5))
        rev11 = storage.lastTransaction()
        self._dostore(storage, oid1, revid=rev11, data=MinPO(7))
        rev12 = storage.lastTransaction()

        time.sleep(2)

        oid2 = storage.new_oid()
        self._dostore(storage, oid2, data=MinPO(10))
        rev21 = storage.lastTransaction()

        oid3 = storage.new_oid()
        self._dostore(storage, oid3, data=MinPO(9))
        rev31 = storage.lastTransaction()

        # (oid1, rev11) garbage-collected
        assertCacheKeys((oid1, rev12), (oid2, rev21), (oid3, rev31))

        self._dostore(storage, oid2, revid=rev21, data=MinPO(11))
        rev22 = storage.lastTransaction()

        time.sleep(2)

        oid4 = storage.new_oid()
        self._dostore(storage, oid4, data=MinPO(11))
        rev41 = storage.lastTransaction()

        # (oid2, rev21) garbage-collected
        assertCacheKeys((oid1, rev12),
                        (oid2, rev22),
                        (oid3, rev31),
                        (oid4, rev41))

    def test_have_MVCC_ergo_no_ReadConflict(self):
        from ZODB.DB import DB
        from ZODB.tests.MinPO import MinPO
        storage = self._makeOne()
        db = DB(storage)
        ob = self._do_read_conflict(db, True)
        self.assertEqual(ob.__class__, MinPO)
        self.assertEqual(getattr(ob, 'child1', MinPO()).value, 'child1')
        self.assertFalse(getattr(ob, 'child2', None))

    def test_load_ex_matches_load(self):
        from ZODB.tests.MinPO import MinPO
        storage = self._makeOne()
        oid = storage.new_oid()
        self._dostore(storage, oid, data=MinPO(1))
        loadp, loads = storage.load(oid, 'whatever')
        exp, exs, exv = storage.loadEx(oid, 'whatever')
        self.assertEqual(loadp, exp)
        self.assertEqual(loads, exs)
        self.assertEqual(exv, '')


def test_suite():
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromTestCase(
            TemporaryStorageTests),
        unittest.defaultTestLoader.loadTestsFromTestCase(ZODBProtocolTests),
    ))
