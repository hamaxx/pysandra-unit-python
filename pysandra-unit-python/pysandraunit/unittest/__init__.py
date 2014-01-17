"""
	Python unittest CassandraTestCase
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	Python unittest TestCase which starts Cassandra server on the first setUp and reloads data for every test case
"""

__all__ = ['CassandraTestCase', 'CassandraTestCaseConfigException']

from unittest import TestCase

from pysandraunit.testcasebase import CassandraTestCaseBase
from pysandraunit.testcasebase import CassandraTestCaseConfigException


class CassandraTestCase(TestCase, CassandraTestCaseBase):

	_settings=None

	@classmethod
	def set_global_settings(cls, settings):
		"""
		Set pysandraunit settings

		:param settings: module or class with pysandraunit configuration

		Accepted options are:

		PYSANDRA_SCHEMA_FILE_PATH = 'path_to_schema'

		PYSANDRA_TMP_DIR = '/tmp/path'

		PYSANDRA_RPC_PORT = port

		PYSANDRA_NATIVE_TRANSPORT_PORT = port

		PYSANDRA_CASSANDRA_YAML_OPTIONS = {}
		"""
		cls._settings = settings

	def setUp(self):
		self._start_cassandra()
		super(CassandraTestCase, self).setUp()

	def tearDown(self):
		super(CassandraTestCase, self).tearDown()
		self._clean_cassandra()

