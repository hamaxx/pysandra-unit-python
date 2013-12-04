##Pysandra Unit

Python wrapper for [cassandra-unit](https://github.com/jsevellec/cassandra-unit)

###Build pysandra-unit jar:

pysandra-unit is a Maven project.

Building it is as simple as:

    cd pysandra-unit
    mvn package


###Using pysandra-unit-python:

    python pysandra-unit-python/setup.py install


    from pysandraunit import PysandraUnit

    pysandra_unit = PysandraUnit('path_to_cassandra_schema.yaml[1]')

    pysandra_unit.start() # Starts cassandra server and loads schema
    pysandra_unit.clean() # Cleans data and reload schema

[1] Docs for schema yaml: https://github.com/jsevellec/cassandra-unit/wiki/How-to-create-a-yaml-dataset

