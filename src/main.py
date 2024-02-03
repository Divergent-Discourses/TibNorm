import os
from configparser import ConfigParser
from module import load_texts, load_tables, normalisation, export_text

# TODO: ང་ normalisation does not work in norm_table3. -> It seems to work -> check again
# TODO: Exceptions of ཀ། and ག།
# TODO: paragraph identification, try out with 1761186 where tabs are missing.

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