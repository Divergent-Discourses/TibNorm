import os
from configparser import ConfigParser
from module import load_texts, load_tables, normalisation, export_text

# TODO: texts, the order of the texts 0001->0002 or p.1->p.2

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