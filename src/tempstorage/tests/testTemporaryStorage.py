import unittest

from ZODB.tests import StorageTestBase
from ZODB.tests import BasicStorage
from ZODB.tests import Synchronization
from ZODB.tests import ConflictResolution
from ZODB.tests import Corruption
from ZODB.tests import MTStorage


class TemporaryStorageTests(StorageTestBase.StorageTestBase,
                           # not a revision storage, but passes
                           #RevisionStorage.RevisionStorage,
                            BasicStorage.BasicStorage,
                            Synchronization.SynchronizedStorage,
                            ConflictResolution.ConflictResolvingStorage,
                            MTStorage.MTStorage,
                           ):

    def open(self, **kwargs):
        from tempstorage.TemporaryStorage import TemporaryStorage
        self._storage = TemporaryStorage('foo')

    def setUp(self):
        StorageTestBase.StorageTestBase.setUp(self)
        self.open()

    def tearDown(self):
        StorageTestBase.StorageTestBase.tearDown(self)

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
        ignored = r2["p"] # force a read to unghostify the root.

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

    def checkConflictCacheIsCleared(self):
        import time
        from ZODB.tests.MinPO import MinPO
        self._storage._conflict_cache_gcevery = 1 # second
        self._storage._conflict_cache_maxage = 1  # second

        oid = self._storage.new_oid()
        self._dostore(oid, data=MinPO(5))

        time.sleep(2)

        oid2 = self._storage.new_oid()
        self._dostore(oid2, data=MinPO(10))

        oid3 = self._storage.new_oid()
        self._dostore(oid3, data=MinPO(9))

        self.assertEqual(len(self._storage._conflict_cache), 2)

        time.sleep(2)

        oid4 = self._storage.new_oid()
        self._dostore(oid4, data=MinPO(11))

        self.assertEqual(len(self._storage._conflict_cache), 1)

    def checkWithMVCCDoesntRaiseReadConflict(self):
        from ZODB.DB import DB
        from ZODB.tests.MinPO import MinPO
        db = DB(self._storage)
        ob = self._do_read_conflict(db, True)
        self.assertEquals(ob.__class__, MinPO)
        self.assertEquals(getattr(ob, 'child1', MinPO()).value, 'child1')
        self.failIf(getattr(ob, 'child2', None))

    def checkLoadEx(self):
        from ZODB.tests.MinPO import MinPO
        oid = self._storage.new_oid()
        self._dostore(oid, data=MinPO(1))
        loadp, loads  = self._storage.load(oid, 'whatever')
        exp, exs, exv = self._storage.loadEx(oid, 'whatever')
        self.assertEqual(loadp, exp)
        self.assertEqual(loads, exs)
        self.assertEqual(exv, '')
        

def test_suite():
    # Note:  we follow the ZODB 'check' pattern here so that the base
    # class tests are picked up.
    return unittest.TestSuite((
        unittest.makeSuite(TemporaryStorageTests, 'check'),
        # Why are we testing this here?
        unittest.makeSuite(Corruption.FileStorageCorruptTests, 'check'),
    ))
