import os
import pycassa

import unittest

from ..pysandraunit import PysandraUnit, PysandraUnitServerError

_here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

class CassandraPool(object):

	def __init__(self, keyspace, servers):
		self._pool = pycassa.pool.ConnectionPool(
			keyspace = keyspace,
			server_list = servers,
			credentials = {
				'username': 'test',
				'password': 'test',
			},
			timeout = 2,
			pool_size = 2,
		)

	def cf_connect(self, cf_name):
		return pycassa.ColumnFamily(
				self._pool,
				column_family = cf_name,
				read_consistency_level = pycassa.ConsistencyLevel.ONE,
				write_consistency_level = pycassa.ConsistencyLevel.ONE,
			)

class BasicOperationsTest(unittest.TestCase):

	def setUp(self):
		self.test_schema = _here('test_schema.yaml')

	def test_start_clean_stop_no_schema(self):
		p = PysandraUnit()
		p.start()
		p.clean()
		p.stop()

	def test_start_clean_connect_stop(self):
		p = PysandraUnit(self.test_schema)
		servers = p.start()

		cp = CassandraPool('testks', servers)
		cp.cf_connect('ascii')

		p.clean()
		p.stop()

	def test_specify_rpc_port(self):
		port = 9999
		host = 'localhost:%s' % port

		p = PysandraUnit(self.test_schema, rpc_port=port)
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
		p2.stop()

