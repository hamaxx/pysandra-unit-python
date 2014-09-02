import os

from ..unittest import TestCase

import pycassa

from ..pysandraunit import PysandraUnit, PysandraUnitServerError
from utils import CassandraPool

_here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

class BasicOperationsTest(TestCase):

    def setUp(self):
        self.test_schema_yaml = _here('test_schema.yaml')
        self.test_schema_cql = _here('test_schema.cql')

    def test_start_clean_stop_no_schema(self):
        p = PysandraUnit()
        p.start()
        p.clean()
        p.stop()

    def test_start_clean_connect_stop(self):
        p = PysandraUnit(self.test_schema_yaml)
        servers = p.start()

        cp = CassandraPool('testks', servers)
        cp.cf_connect('ascii')

        p.clean()
        p.stop()

    def test_specify_rpc_port(self):
        port = 9999
        host = 'localhost:%s' % port

        p = PysandraUnit(self.test_schema_yaml, rpc_port=port)
        servers = p.start()

        self.assertEqual(servers[0], host)

        cp = CassandraPool('testks', [host])
        cp.cf_connect('ascii')

        p.stop()


    def test_double_start(self):
        p1 = PysandraUnit()
        p2 = PysandraUnit()

        p1.start()
        self.assertRaises(PysandraUnitServerError, p1.start)
        self.assertRaises(PysandraUnitServerError, p2.start)
        p1.stop()

        p2.start()
        p2.stop()

    def test_cql_schema(self):
        port = 9999
        host = 'localhost:%s' % port

        p = PysandraUnit(self.test_schema_cql, rpc_port=port)
        servers = p.start()

        self.assertEqual(servers[0], host)

        cp = CassandraPool('testks', [host])
        cp.cf_connect('ascii')

        p.stop()

    def test_local_quorum(self):
        p = PysandraUnit(self.test_schema_cql)
        servers = p.start()

        cp = CassandraPool('testks', servers)
        cf = cp.cf_connect('ascii')

        self.assertRaises(pycassa.NotFoundException, cf.get, 'test_key', read_consistency_level=pycassa.ConsistencyLevel.LOCAL_QUORUM)

        p.stop()
