"""
	Django CassandraTestCase
	~~~~~~~~~~~~~~~~~~~~~~~~

	Django TestCase which starts Cassandra server on the first setUp and reloads data for every test case
"""

__all__ = ['CassandraTestCase', 'CassandraTestCaseConfigException']

from django.test import TestCase
from django.conf import settings

from pysandraunit.testcasebase import CassandraTestCaseBase
from pysandraunit.testcasebase import CassandraTestCaseConfigException


class CassandraTestCase(TestCase, CassandraTestCaseBase):

	_settings=settings

