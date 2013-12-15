import pycassa

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

