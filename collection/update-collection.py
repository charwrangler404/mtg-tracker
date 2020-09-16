#!/usr/bin/env python3

import argparse, csv, scrython, sqlite3

parser = argparse.ArgumentParser('update-collection.py')
parser.add_argument('--add', nargs='?', help='Card name to add')
parser.add_argument('--remove', nargs='?', help='Card name to remove')
parser.add_argument('-n', default=1, nargs='?', help='Number of cards to add/remove, defaults to 1')
parser.add_argument('--update', nargs='?', help='Card to update')
parser.add_argument('collection', default='paper', nargs='?', help='Collection to update [PAPER/mtgo]')
args = parser.parse_args()

db_file = 'database/collection.db'
add_card = args.add
remove_card = args.remove
no_of_cards = args.n
update_card = args.update
table_name = args.collection

def update_collection(action, db_file, card, no_of_cards):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    if action.lower() == 'add':
        query = f'INSERT INTO "{table_name}" VALUES ("{no_of_cards}", "{card}")'
        print(query)
        c.execute(query)
        conn.commit()
        print(f'Added {no_of_cards} of card {card} to the databse' )

    elif action.lower() == 'remove':
        query = f'DELETE FROM "{table_name}" WHERE name = "{remove_card}"'
        print(query)
        c.execute(query)
        conn.commit()
        print(f'Removed {card} from the databse')

    elif action.lower() == 'update':
        query = f'SELECT * from "{table_name}" WHERE name = "{card}"'
        output = c.execute(query)
        if output.fetchone() != None:
            print(f'Card {card} exists')
            query = f'UPDATE "{table_name}" SET quantity = "{no_of_cards}" WHERE name = "{card}"'
            print(query)
            c.execute(query)
            conn.commit()
            print(f'Updated card {update_card} to quantity {no_of_cards}')
        else:
            print(f'Card {card} is not in the database')


    else:
        print(f'Error: Specify an action to take on the database')

    conn.close()
    

def main():
    if add_card:
        print(f"Adding {no_of_cards} copies of {add_card} to collection {table_name}")
        update_collection('add', db_file, add_card, no_of_cards)

    elif remove_card:
        print(f"Removing {remove_card} from collection {table_name}")
        update_collection('remove', db_file, remove_card, no_of_cards)

    elif update_card:
        print(f"Updating card {update_card} to quantity {no_of_cards} in collection {table_name}")
        update_collection('update', db_file, update_card, no_of_cards)

    else:
        print("Error: Specify a card name to add or remove")


main()
