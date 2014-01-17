##Pysandra Unit

Write isolated unit/integration tests with Cassandra in Django and other python applications.

Pysandra Unit is a Python wrapper around [cassandra-unit](https://github.com/jsevellec/cassandra-unit).


###Install:

    pip install pysandra-unit

    or

    python pysandra-unit-python/setup.py install


###Docs:

[pysandra-unit docs](http://pythonhosted.org/pysandra-unit/)

[Uning Django TestCase](http://pythonhosted.org/pysandra-unit/modules/django.html)

[Uning Unittest TestCase](http://pythonhosted.org/pysandra-unit/modules/unittest.html)



###Running pysandraunit tests

	pip install -r pysandraunit/tests/requirements.txt

	./run_tests.sh


###Build pysandra-unit jar:

pysandra-unit is a Maven project.

Building it is as simple as:

    cd pysandra-unit
    mvn package

