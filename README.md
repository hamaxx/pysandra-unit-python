##Pysandra Unit

Python wrapper for [cassandra-unit](https://github.com/jsevellec/cassandra-unit)

###Build pysandra-unit jar:

pysandra-unit is a Maven project.

Building it is as simple as:

    cd pysandra-unit
    mvn package


###Using pysandra-unit-python:

Install:

    pip install pysandra-unit

    or

    python pysandra-unit-python/setup.py install


Run in Python:

    from pysandraunit import PysandraUnit

    pysandra_unit = PysandraUnit('path_to_cassandra_schema.yaml[1]')

    pysandra_unit.start() # Starts cassandra server and loads schema
    pysandra_unit.clean() # Cleans data and reload schema

Django Test Case:

	from pysandraunit import CassandraTestCase

	class SimpleTest(CassandraTestCase):

		def setUp(self):
			test_cassandra_server_list = self.cassandra_server_list
			...


[1] Docs for schema yaml: https://github.com/jsevellec/cassandra-unit/wiki/How-to-create-a-yaml-dataset

