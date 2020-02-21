#!/usr/bin/env python3

import sqlite3, argparse, scrython, re

parser = argparse.ArgumentParser('get-prices.py')
parser.add_argument('cardname', type=str, help='Card name to query database for')
parser.add_argument('setname', default='', nargs='?', help='Set identifier')
parser.add_argument('database', help='Path to the prices database', default='database/prices.db', nargs='?')
parser.add_argument('--latest', '-l', type=bool, default=False, help='Return only the latest price', nargs='?')
parser.add_argument('--average', type=bool, default=False, help='Return the latest avergae price between sets', nargs='?')
args = parser.parse_args()

cardname = args.cardname
db_file = args.database
set_id = args.setname

def get_latest(cardname):
    data = scrython.cards.Search('++{}'.format(cardname))
    for card in data.data():
        print('''Name: {}
        Set: {}
        Price: {}
        Foil: {}
        Tix: {}'''.format(card['name'], card['set'], card['prices']['usd'], card['prices']['usd_foil'],
                          card['prices']['tickets']))
        print('=====================')

#get_latest(cardname)

def get_tables():
    tables = []
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(query)
    for table_obj in c.fetchall():
        table_s1 = re.sub('^..', '', str(table_obj))
        table = re.sub('...$', '', str(table_s1))
        tables.append(table)
    conn.close()
    return tables

def print_historic(cardname, set_id):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    for table in get_tables():
        if set_id == '':
            query = 'SELECT * FROM %s WHERE cardname="%s";' % (table, cardname)
        else:
            query = 'SELECT * FROM %s WHERE cardname="%s" AND setname="%s";' % (table, cardname, set_id)

        prices = c.execute(query)
        for line in prices:
            print(table + ' : ' + str(line))
    conn.close()

print_historic(cardname, set_id)
