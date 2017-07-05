#!/usr/bin/env python

import sqlite3

def create_connection(db_file):
	"""Create a connection to db_file database."""
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except sqlite3.Error as e:
		print(e)

def main():
	"""Main function."""

	annotations = [
		'dann',
		'eigen'
	]

	

	database = 'annotation.db'

	conn = create_connection(database)



if __name__ == '__main__':
	main()
