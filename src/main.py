import os
from configparser import ConfigParser
from module import load_texts, load_tables, normalisation, export_text

# TODO: paragraph identification, try out with 1761186 where tabs are missing.
# TODO: check Ta and Da are successfully replaced.

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