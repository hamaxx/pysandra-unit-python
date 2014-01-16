from pysandraunit import PysandraUnit

_pysandra_single = None
_cassandra_server_list = None



class CassandraTestCaseConfigException(Exception):
	pass

class CassandraTestCaseBase(object):
	"""
	Django TestCase which starts Cassandra server on the first setUp and reloads data for every test case
	"""

	def _init_cassandra(self):
		global _pysandra_single

		if not self._settings:
			_pysandra_single = PysandraUnit()
		else:
			schema_path = getattr(self._settings, 'PYSANDRA_SCHEMA_FILE_PATH', None)
			tmp_dir = getattr(self._settings, 'PYSANDRA_TMP_DIR', None)
			rpc_port = getattr(self._settings, 'PYSANDRA_RPC_PORT', None)
			native_transport_port = getattr(self._settings, 'PYSANDRA_NATIVE_TRANSPORT_PORT', None)
			cassandra_yaml_options = getattr(self._settings, 'PYSANDRA_CASSANDRA_YAML_OPTIONS', None)

			_pysandra_single = PysandraUnit(schema_path, tmp_dir, rpc_port, native_transport_port, cassandra_yaml_options)

		return _pysandra_single.start()


	def _start_cassandra(self):
		global _pysandra_single, _cassandra_server_list

		if not _pysandra_single:
			_cassandra_server_list = self._init_cassandra()

		self.cassandra_server_list = _cassandra_server_list

	def _clean_cassandra(self):
		if not _pysandra_single:
			return

		_pysandra_single.clean()

