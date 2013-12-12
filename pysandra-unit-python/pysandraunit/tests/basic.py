import os

import unittest

from ..pysandraunit import PysandraUnit

_here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

class BasicOperationsTest(unittest.TestCase):

	def setUp(self):
		self.test_schema = _here('test_schema.yaml')

	def test_start_clean_stop(self):
		p = PysandraUnit(self.test_schema)
		p.start()
		p.clean()
		p.stop()
