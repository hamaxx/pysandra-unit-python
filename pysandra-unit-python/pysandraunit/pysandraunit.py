import subprocess
import os
import json

_here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

_PYSANDRA_COMMAND_START = 'start'
_PYSANDRA_COMMAND_STOP = 'stop'
_PYSANDRA_COMMAND_LOAD_DATA = 'load'
_PYSANDRA_COMMAND_CLEAN_DATA = 'clean'

_PYSANDRA_JAR_PATH = _here('jar/pysandra-unit.jar')


class PysandraUnitServerError(Exception): pass

class PysandraUnit(object):

	_dataset_path = None
	_server = None

	def __init__(self, dataset_path):
		self._dataset_path = dataset_path

	def _run_pysandra(self):
		self._server = subprocess.Popen(["java", "-jar", _PYSANDRA_JAR_PATH], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

	def _get_command_message(self, msg):
		return '%s\n' % json.dumps(msg)

	def _run_command(self, command, param=None, join=False):
		if not self._server or self._server.stdin.closed or self._server.stdout.closed:
			raise PysandraUnitServerError('Pysandra server not running')

		msg = {
			'command': command,
			'param': param or {},
		}

		if join:
			response_str = self._server.communicate(self._get_command_message(msg))[0].strip()
		else:
			self._server.stdin.write(self._get_command_message(msg))
			response_str = self._server.stdout.readline().strip()

		try:
			response = json.loads(response_str)
		except Exception:
			raise PysandraUnitServerError('Invalid pysandra server response: %s' % response_str)

		if response.get('status') == 'ok':
			return response.get('value');

		raise PysandraUnitServerError(response)

	def start(self):
		self._run_pysandra()

		server = self._run_command(_PYSANDRA_COMMAND_START)
		self._run_command(_PYSANDRA_COMMAND_LOAD_DATA, {
			'filename': self._dataset_path
		})

		return [server]

	def stop(self):
		self._run_command(_PYSANDRA_COMMAND_STOP, join=True)
		self._server = None

	def clean(self):
		self._run_command(_PYSANDRA_COMMAND_CLEAN_DATA)
		self._run_command(_PYSANDRA_COMMAND_LOAD_DATA, {
			'filename': self._dataset_path
		})

