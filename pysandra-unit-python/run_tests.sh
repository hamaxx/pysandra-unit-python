#!/bin/bash

python -m unittest pysandraunit.tests.basic
python -m unittest pysandraunit.tests.django
python -m unittest pysandraunit.tests.unittest
