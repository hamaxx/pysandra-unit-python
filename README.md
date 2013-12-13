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
    pysandra_unit.stop() # Sends a stop singnal and waits for server to die

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


###PysandraUnit docs

class PysandraUnit(__builtin__.object)
	Methods defined here:
	
	__init__(self, dataset_path=None, tmp_dir=None, rpc_port=None, cassandra_yaml_options=None)
		Construct a PysandraUnit object. Java server won't be started yet
		
		:param dataset_path: path to the dataset file in yaml format. Check cassandra-unit docs for details
		:param tmp_dir: path to the directory where PysandraUnit and Cassandra should create temporary files
		:param rpc_port: Cassandra rpc port
		:prama cassandra_yaml_options: dict of additional options passed to Cassandra in cassandra.yaml file
	
	clean(self)
		Cleans all Cassandra Keyspaces and reloads data if dataset is provided in constructor
		If server is not running, 'PysandraUnitServerError' exception will be raised
	
	get_cassandra_host(self)
		Returns Cassandra server host and rpc port in format: 'localhost:9710'
	
	load_data(self, dataset_path=None)
		Load schema into Cassandra from dataset file
		If file isn't provided the one from constructior will be used
		
		:param dataset_path: path to the dataset file in yaml format. Check cassandra-unit docs for details
	
	start(self)
		Start Pysandra and Cassandra server, loads dataset file if provided in the constructor
		If server is already running, 'PysandraUnitServerError' exception will be raised
	
	stop(self)
		Stop Pysandra and Cassandra server if running
