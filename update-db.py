#!/usr/bin/env python3

import argparse, csv, scrython, sqlite3
from time import sleep, time, ctime


parser = argparse.ArgumentParser('update-db.py')
parser.add_argument('database', default='database/', nargs='?', help='Database to update')
parser.add_argument('watchlist', default='conf/watchlist.conf', nargs='?', help='Watchlist to check against')
args = parser.parse_args()

runtime = ctime(time())
db_file = args.database
watchfile = args.watchlist

conn = sqlite3.connect(db_file)
c = conn.cursor()

def get_price(watchfile):
    cards = []
    with open(watchfile, 'r') as watch_db:
        for cardname in watch_db.readlines():
            print('Fetching ' + cardname, end='')
            if cardname != '':
                sleep(0.1)
                try:
                    data = scrython.cards.Search(q='++{}'.format(cardname), order='alphabetical')
                    for card in data.data():
                        card_obj = (card['name'], card['set'].upper(), card['prices'])
                        cards.append(card_obj)
                except ValueError:
                    print('Invalid Card name')
    return cards


def update_database(cards):
    print('stuff')

cards = get_price(watchfile)
for line in cards:
    print(line)
