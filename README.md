##Pysandra Unit

Python wrapper for [cassandra-unit](https://github.com/jsevellec/cassandra-unit).

Pyssandra Unit helps you write isolated unittests in Django and other python applications.

###Install:

    pip install pysandra-unit

    or

    python pysandra-unit-python/setup.py install


###Run in Python:

    from pysandraunit import PysandraUnit

    pysandra_unit = PysandraUnit('path_to_cassandra_schema.yaml[1]')

    pysandra_unit.start() # Starts cassandra server and loads schema
    pysandra_unit.clean() # Cleans data and reload schema

###Django Test Case:

settings.py:

	PYSANDRA_SCHEMA_FILE_PATH = 'path_to_schema.yaml[1]'

tests.py:

	from pysandraunit import CassandraTestCase

	class SimpleTest(CassandraTestCase):

		def setUp(self):
			test_cassandra_server_list = self.cassandra_server_list
			...

CassandraTestCase will drop data and reload schema for every test case.

[1] Docs for schema yaml: https://github.com/jsevellec/cassandra-unit/wiki/How-to-create-a-yaml-dataset

###Build pysandra-unit jar:

pysandra-unit is a Maven project.

Building it is as simple as:

    cd pysandra-unit
    mvn package


