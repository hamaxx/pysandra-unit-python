SECRET_KEY = 'pysandraunit'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': ':memory:',					  # Or path to database file if using sqlite3.
	}
}
