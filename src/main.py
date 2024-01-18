import os
import re
from configparser import ConfigParser
from module import load_texts, load_tables, normalization

# TODO: load text by nested dictionary: the first keys are the document names and second keys are page names.
# TODO: Think in which order (table1, table2, ...) the replacement is to be executed.

def main():
    config = ConfigParser()
    config.read('src/config.ini')

    # load replacement tables
    tables = load_tables(config)

    # load texts in which characters are to be normalised.
    texts = load_texts(config)

    # normalize
    normalization(texts, tables)

if __name__ == '__main__':
    main()