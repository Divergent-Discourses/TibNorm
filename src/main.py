import os
import re
from configparser import ConfigParser
from module import load_texts, load_tables, normalization

# TODO: create an export function in main.py
# TODO: create other normalization functions in module.py
# TODO: Think in which order (table1, table2, ...) the replacement is to be executed.

def main():
    config = ConfigParser()
    config.read('src/config.ini')

    # load replacement tables
    tables = load_tables(config)

    # load texts in which characters are to be normalised.
    texts = load_texts(config)

    # normalize
    text_norm = normalization(texts, tables)

if __name__ == '__main__':
    main()