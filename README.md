##Pysandra Unit

Write isolated unit/integration tests with Cassandra in Django and other python applications.

Pysandra Unit is a Python wrapper around [cassandra-unit](https://github.com/jsevellec/cassandra-unit).


###Install:

    pip install pysandra-unit

    or

    python pysandra-unit-python/setup.py install


###Docs:

[pysandra-unit docs](docs/_build/text/index.txt)


###Examples:

####Run in Python:

    from pysandraunit import PysandraUnit

    pysandra_unit = PysandraUnit('path_to_cassandra_schema.yaml/cql/xml/json[1]')

    pysandra_unit.start() # Starts cassandra server and loads schema
    pysandra_unit.clean() # Cleans data and reload schema
    pysandra_unit.stop() # Sends a stop singnal and waits for server to die

Check PysandraUnit docs below for more details.


####Django TestCase:

settings.py:

	PYSANDRA_SCHEMA_FILE_PATH = 'path_to_schema[1]' # optional
	PYSANDRA_TMP_DIR = '/tmp/path' # optional; default is /dev/shm or /tmp
	PYSANDRA_RPC_PORT = port # optional; default is 9171
	PYSANDRA_NATIVE_TRANSPORT_PORT = port # optional; default is 9142
	PYSANDRA_CASSANDRA_YAML_OPTIONS = {} # optional params passed to Cassandra via cassandra.yaml file

tests.py:

	from pysandraunit.django import CassandraTestCase

	class SimpleTest(CassandraTestCase):

		def setUp(self):
			test_cassandra_server_list = self.cassandra_server_list
			...

####Unittest TestCase:

tests.py:

	from pysandraunit.django import CassandraTestCase
	import settings

	CassandraTestCase.set_global_settings(settings) # settings module or class, accepts same options as django

	class SimpleTest(CassandraTestCase):

		def setUp(self):
			test_cassandra_server_list = self.cassandra_server_list
			...

CassandraTestCase will drop data and reload schema for every test case.

[1] Docs for schema files: https://github.com/jsevellec/cassandra-unit/wiki/available-dataset-format


###Running pysandraunit tests

	pip install -r pysandraunit/tests/requirements.txt

	./run_tests.sh


###Build pysandra-unit jar:

pysandra-unit is a Maven project.

Building it is as simple as:

    cd pysandra-unit
    mvn package

