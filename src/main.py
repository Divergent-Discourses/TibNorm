from configparser import ConfigParser
from module import load_texts, load_tables, export_text
from normaliser import Normaliser

def main():
    config = ConfigParser()
    config.read('src/config.ini')

    # load replacement tables
    tables = load_tables(config)

    # load texts in which characters are to be normalised.
    texts = load_texts(config)

    # normalize
    normaliser = Normaliser(texts, tables)
    text_norm = normaliser.normalisation()

    # export
    print("Saving normalised files ...")
    export_text(config, text_norm)

if __name__ == '__main__':
    main()