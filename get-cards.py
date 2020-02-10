#!/usr/bin/env python3

import scrython
import argparse
import csv
import os
from time import sleep, time, ctime

parser = argparse.ArgumentParser('get-cards.py')
args = parser.parse_args()

runtime = ctime(time())
db_name = 'database/prices.tsv'


def read_database(db_file):
    with open(db_file) as tsvfile:
        database = csv.DictReader(tsvfile, delimiter=' ', quotechar='"')
    tsvfile.close()
    return database

def write_database(cards):
    with open(db_name, 'w', newline='') as tsvfile:
        fieldnames = ['name', 'set', runtime]
        writer = csv.DictWriter(tsvfile, dialect='excel-tab', fieldnames=fieldnames)

        writer.writeheader()
        for card in cards:
            writer.writerow({runtime: card[2], 'set': card[1], 'name': card[0]})
        tsvfile.close()

def get_price(watchfile):
    cards = []
    with open(watchfile, 'r') as watch_db:
        for cardname in watch_db.readlines():
            print('Fetching ' + cardname, end='')
            if cardname != '':
                sleep(0.1)
                try:
                    data = scrython.cards.Search(q='++{}'.format(cardname))
                    for card in data.data():
                        card_obj = (card['name'], card['set'].upper(), card['prices'])
                        cards.append(card_obj)
                except ValueError:
                    print('Invalid Card name')

    return cards

cards = get_price('conf/watchlist.conf')
write_database(cards)
