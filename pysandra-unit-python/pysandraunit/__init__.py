"""
	pysandra-unit
	~~~~~

	Python wrapper around cassandra-unit that helps you write isolated unittests in Django and other python applications.
"""

__all__ = ['PysandraUnit', 'PysandraUnitServerError', 'CassandraTestCase', 'CassandraTestCaseConfigException']

from pysandraunit import PysandraUnit, PysandraUnitServerError

import os
if os.environ.get('DJANGO_SETTINGS_MODULE'):
	from pysandraunit_django.testcase import CassandraTestCase, CassandraTestCaseConfigException
