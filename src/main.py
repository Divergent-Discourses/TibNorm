import os
from configparser import ConfigParser
from module import load_texts, load_tables, normalisation, export_text

# TODO: create other normalisation functions in module.py
# TODO: Think in which order (table1, table2, ...) the replacement is to be executed.
# The order of the process: table1 (་།) -> table4 (ང་)

def main():
    config = ConfigParser()
    config.read('src/config.ini')

    # load replacement tables
    tables = load_tables(config)

    # load texts in which characters are to be normalised.
    texts = load_texts(config)

    # normalize
    text_norm = normalisation(texts, tables)

    # export
    export_text(config, text_norm)

if __name__ == '__main__':
    main()