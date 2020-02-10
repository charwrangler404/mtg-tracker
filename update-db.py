#!/usr/bin/env python3

import argparse, csv, scrython
from time import sleep, time, ctime


parser = argparse.ArgumentParser('update-db.py')
parser.add_argument('database', default='database/prices.working.tsv', nargs='?', help='Database to update')
args = parser.parse_args()

runtime = ctime(time())
db_file = args.database

print('Opening database for reading')
with open(db_file, 'rw') as tsvinput:
    writer = csv.writer(db_file)
