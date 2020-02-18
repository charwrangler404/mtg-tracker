#!/usr/bin/env python3

import sqlite3. argparse, scrython

parser = argparse.ArgumentParser('get-prices.py')
parser.add_argument('cardname', type=str, help='Card name to query database for')
parser.add_argument('--latest', '-l', type=bool, default=False, help='Return only the latest price', nargs='?')
parser.add_argument('--average', type=bool, default=False, help='Return the latest avergae price between sets'. nargs='?')
args = parser.parse_args()

def get_latest(cardname):
    
