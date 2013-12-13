import subprocess
import os
import json
import yaml
import shutil


_here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)


_COMMAND_START = 'start'
_COMMAND_STOP = 'stop'
_COMMAND_LOAD_DATA = 'load'
_COMMAND_CLEAN_DATA = 'clean'

_DEFAULT_RPC_HOST = 'localhost'
_DEFAULT_RPC_PORT = 9171

_TMP_PATHS = ['/dev/shm/', '/tmp/', './']
_TMP_DIR = 'pysandraunittarget/'

_JAR_PATH = _here('jar/pysandra-unit.jar')
_DEFAULT_YAML_PATH = _here('resources/cu-cassandra.yaml')

_CASSANDRA_YAML_REL_PATH = 'cassandra.yaml'
_CASSANDRA_DIR_OPTIONS = {
	'commitlog_directory': 'embeddedCassandra/commitlog',
	'saved_caches_directory': 'embeddedCassandra/saved_caches',
	'data_file_directories': ['embeddedCassandra/data'],
}


class PysandraUnitServerError(Exception): pass

class PysandraUnit(object):

	_dataset_path = None
	_server = None
	_cassandra_yaml = None

	_cassandra_running = False

	tmp_dir = None

	def __init__(self, dataset_path=None, tmp_dir=None, rpc_port=None, cassandra_yaml_options=None):
		"""
		Construct a PysandraUnit object. Java server won't be started yet

		:param dataset_path: path to the dataset file in yaml format. Check cassandra-unit docs for details
		:param tmp_dir: path to the directory where PysandraUnit and Cassandra should create temporary files
		:param rpc_port: Cassandra rpc port
		:prama cassandra_yaml_options: dict of additional options passed to Cassandra in cassandra.yaml file
		"""

		self._dataset_path = dataset_path

		self.tmp_dir = tmp_dir or self._find_tmp_dir()
		self._create_tmp_dir()

		self.rpc_port = rpc_port or _DEFAULT_RPC_PORT

		self._cassandra_yaml = self._get_yaml_file(cassandra_yaml_options)

	def _create_tmp_dir(self):
		if os.path.exists(self.tmp_dir):
			shutil.rmtree(self.tmp_dir)
		os.makedirs(self.tmp_dir, 0o755)

	def _find_tmp_dir(self):
		for path in _TMP_PATHS:
			if not os.path.exists(path):
				continue
			if not os.path.isdir(path):
				continue
			if not os.access(path, os.W_OK):
				continue

			full_path = os.path.join(path, _TMP_DIR)
			return full_path

		return None

	def _get_yaml_file(self, yaml_options):
		config = yaml.load(open(_DEFAULT_YAML_PATH, 'r'))

		for opt, c_dirs in _CASSANDRA_DIR_OPTIONS.iteritems():
			if isinstance(c_dirs, list):
				config[opt] = [os.path.join(self.tmp_dir, c_dir) for c_dir in c_dirs]
			else:
				config[opt] = os.path.join(self.tmp_dir, c_dirs)

		config['rpc_port'] = self.rpc_port

		if yaml_options:
			for k, v in yaml_options:
				config[k] = v

		new_yaml_path = os.path.join(self.tmp_dir, _CASSANDRA_YAML_REL_PATH)

		with open(new_yaml_path, 'w') as fw:
			fw.write(yaml.dump(config, default_flow_style=False))

		return new_yaml_path

	def _run_pysandra(self):
		self._server = subprocess.Popen(["java", "-jar", _JAR_PATH], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

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

		if not response_str:
			try:
				error_msg = self._server.stderr.readline()
			except ValueError:
				error_msg = 'Unknown error'
			raise PysandraUnitServerError('Failed to execute command %s: %s' % (command, error_msg))

		try:
			response = json.loads(response_str)
		except Exception:
			raise PysandraUnitServerError('Invalid pysandra server response: %s' % response_str)

		if response.get('status') == 'ok':
			return response.get('value');

		raise PysandraUnitServerError(response)

	def get_cassandra_host(self):
		"""
		Returns Cassandra server host and rpc port in format: 'localhost:9710'
		"""

		return '%s:%s' % (_DEFAULT_RPC_HOST, self.rpc_port)

	def load_data(self, dataset_path=None):
		"""
		Load schema into Cassandra from dataset file
		If file isn't provided the one from constructior will be used

		:param dataset_path: path to the dataset file in yaml format. Check cassandra-unit docs for details
		"""

		dataset_path = dataset_path or self._dataset_path
		if not dataset_path:
			raise PysandraUnitServerError('Can\'t load data. No dataset specified.')

		self._run_command(_COMMAND_LOAD_DATA, {
			'filename': self._dataset_path,
			'host': self.get_cassandra_host(),
		})

	def start(self):
		"""
		Start Pysandra and Cassandra server, loads dataset file if provided in the constructor
		If server is already running, 'PysandraUnitServerError' exception will be raised
		"""

		if self._cassandra_running:
			raise PysandraUnitServerError('Cassandra server already running')

		self._run_pysandra()

		self._run_command(_COMMAND_START, {
			'tmpdir': self.tmp_dir,
			'yamlconf': self._cassandra_yaml,
		})

		if self._dataset_path:
			self.load_data();

		self._cassandra_running = True

		return [self.get_cassandra_host()]

	def stop(self):
		"""
		Stop Pysandra and Cassandra server if running
		"""

		if self._cassandra_running:
			self._run_command(_COMMAND_STOP, join=True)

		self._server = None
		self._cassandra_running = False

	def clean(self):
		"""
		Cleans all Cassandra Keyspaces and reloads data if dataset is provided in constructor
		If server is not running, 'PysandraUnitServerError' exception will be raised
		"""

		if not self._cassandra_running:
			raise PysandraUnitServerError('Cassandra server not running')

		self._run_command(_COMMAND_CLEAN_DATA)
		if self._dataset_path:
			self.load_data();
