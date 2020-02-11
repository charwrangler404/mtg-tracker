#!/usr/bin/env python3

import argparse, csv, scrython, sqlite3
from time import sleep, time, ctime


parser = argparse.ArgumentParser('update-db.py')
parser.add_argument('database', default='database/prices.db', nargs='?', help='Database to update')
parser.add_argument('--cardlist', default='conf/cardlist.conf', help='Card list to check against')
parser.add_argument('--setlist', default='conf/setlist.conf', help='Set list to check against')
args = parser.parse_args()

runtime = ctime(time())
db_file = args.database

def cardlist_get(config):
    cards_usd = []
    cards_foil = []
    with open(config, 'r') as watch_db:
        for cardname in watch_db.readlines():
            print('Fetching ' + cardname, end='')
            if cardname != '':
                sleep(0.1)
                try:
                    data = scrython.cards.Search(q='++{}'.format(cardname), order='alphabetical')
                    for card in data.data():
                        card_obj_usd = (card['name'], card['set'].upper(), card['prices']['usd'])
                        cards_usd.append(card_obj_usd)
                        card_obj_foil = (card['name'], card['set'].upper(), card['prices']['usd_foil'])
                        cards_foil.append(card_obj_foil)
                except ValueError:
                    print('Invalid Card name: ' + cardname)
    return cards_usd, cards_foil

def setlist_get(config):
    cards_usd = []
    cards_foil = []
    with open (config, 'r') as setlist:
            for setname in setlist.readlines():
                if setname != '':
                    try:
                        sleep(0.1)
                        data = scrython.cards.Search(q='s:{}'.format(setname))
                        for card in data.data():
                            card_obj_usd = (card['name'], card['set'].upper(), card['prices']['usd'])
                            card_obj_foil = (card['name'], card['set'].upper(), card['prices']['usd_foil'])
                            cards_usd.append(card_obj_usd)
                            cards_foil.append(card_obj_foil)
                    except ValueError:
                        print('Invalid Set name: ' + setname)
    return cards_usd, cards_foil

def update_database(cards_usd, cards_foil):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    for card in cards_usd:
        print('Updating database cards_usd with values :' + str(card))
        c.execute('INSERT INTO cards_usd VALUES (?,?,?);', card)
        conn.commit()
    print('Database cards_usd successfully updated')
    for card in cards_foil:
        print('Updating database cards_foil with card: ' + str(card))
        c.execute('INSERT INTO cards_foil VALUES (?,?,?);', card)
        conn.commit()
    print('Database cards_foil successfully updated')
    conn.close()

#cards_usd, cards_foil = cardlist_get(args.cardlist)
#update_database(cards_usd, cards_foil)
cards_usd, cards_foil = setlist_get(args.setlist)
update_database(cards_usd, cards_foil)
