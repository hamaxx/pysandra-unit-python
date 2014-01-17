.. toctree::
   :maxdepth: 2

.. automodule:: pysandraunit.django

.. autoclass:: CassandraTestCase
   :members:

.. autoexception:: CassandraTestCaseConfigException

.. describe:: django settings.py options

PYSANDRA_SCHEMA_FILE_PATH = 'path_to_schema'

PYSANDRA_TMP_DIR = '/tmp/path' -- default is /dev/shm or /tmp

PYSANDRA_RPC_PORT = 9171

PYSANDRA_NATIVE_TRANSPORT_PORT = 9142

PYSANDRA_CASSANDRA_YAML_OPTIONS = {} -- optional params passed to Cassandra via cassandra.yaml file
