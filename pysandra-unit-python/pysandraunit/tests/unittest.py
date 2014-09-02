import os
import pycassa

from utils import CassandraPool

_here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

from pysandraunit.tests import django_settings as settings

from ..unittest import CassandraTestCase


CassandraTestCase.set_global_settings(settings)

class BasicOperationsTest(CassandraTestCase):

    @classmethod
    def setUpClass(cls):
        settings.PYSANDRA_SCHEMA_FILE_PATH = _here('test_schema.yaml')

    @classmethod
    def tearDownClass(cls):
        settings.PYSANDRA_SCHEMA_FILE_PATH = None

    def test_connect_clean_1(self):
        self.assertEqual(self.cassandra_server_list, ['localhost:9171'])

        cp = CassandraPool('testks', self.cassandra_server_list)
        cf = cp.cf_connect('ascii')

        self.assertRaises(pycassa.NotFoundException, cf.get, 'test')

        cf.insert('test', {'case': 'a'})
        self.assertEqual(cf.get('test'), {'case': 'a'})

    def test_connect_clean_2(self):
        self.assertEqual(self.cassandra_server_list, ['localhost:9171'])

        cp = CassandraPool('testks', self.cassandra_server_list)
        cf = cp.cf_connect('ascii')

        self.assertRaises(pycassa.NotFoundException, cf.get, 'test')

        cf.insert('test', {'case': 'a'})
        self.assertEqual(cf.get('test'), {'case': 'a'})

