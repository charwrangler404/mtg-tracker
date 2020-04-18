#!/usr/bin/env python3

import argparse, csv, scrython, sqlite3
from time import sleep, strftime


parser = argparse.ArgumentParser('update-db.py')
parser.add_argument('database', default='database/prices.db', nargs='?', help='Database to update')
parser.add_argument('--cardlist', default='conf/cardlist.conf', help='Card list to check against')
parser.add_argument('--setlist', default='conf/setlist.conf', help='Set list to check against')
args = parser.parse_args()

runtime = strftime('%b_%m_%d_%H')
db_file = args.database

def cardlist_get(config):
    cards = []
    with open(config, 'r') as watch_db:
        for cardname in watch_db.readlines():
            print('Fetching ' + cardname, end='')
            if cardname != '':
                sleep(0.1)
                try:
                    data = scrython.cards.Search(q='++{}'.format(cardname))
                    for card in data.data():
                        card_obj = (card['name'], card['set'].upper(), card['prices']['usd'], card['prices']['usd_foil'])
                        cards.append(card_obj)
                except ValueError:
                    print('Invalid Card name: ' + cardname)
    return cards

def setlist_get(config):
    cards = []
    with open (config, 'r') as setlist:
            for setname in setlist.readlines():
                if setname != '':
                    try:
                        sleep(0.1)
                        data = scrython.cards.Search(q='s:{}'.format(setname))
                        for card in data.data():
                            card_obj = (card['name'], card['set'].upper(), card['prices']['usd'], card['prices']['usd_foil'])
                            cards.append(card_obj)
                    except ValueError:
                        print('Invalid Set name: ' + setname)
    return cards

# Query scryfall for cards and return a list of tuples
def cards_get(config, list_type):
    cards = []
    with open (config, 'r') as qlist:
        for name in qlist.readlines():
            if list_type == 'setlist':
                query = 's:{}'.format(name)
            elif list_type == 'watchlist':
                query = '++{}'.format(name)
            else:
                print('Error: Invalid list type')
                break
            if name != '':
                try:
                    data = scrython.cards.Search(q=query)
                    for card in data.data():
                        card_obj = (card['name'], card['set'], card['prices']['usd'], card['prices']['usd_foil'])
                    cards.append(card_obj)
                except ValueError:
                    print('Error: invalid query: ' + name)
    return cards

def create_table(table_name):
    query = 'CREATE TABLE %s (cardname, setname, price_usd, price_foil);' % table_name
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()

# Update the table defined as table_name after it has been created
def update_database(cards, table_name):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    for card in cards:
        print('Updating database %s with values %s:' % (table_name, card))
        query = 'INSERT INTO %s VALUES (?,?,?,?);' % table_name
        c.execute(query, card)
        conn.commit()
    print('Database %s successfully updated' % table_name)
    conn.close()


create_table(runtime)
cards = cardlist_get(args.cardlist)
update_database(cards, runtime)
cards = setlist_get(args.setlist)
update_database(cards, runtime)
