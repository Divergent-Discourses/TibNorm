import glob
import os
import pandas as pd

def load_tables(config):
    tables = {}
    pattern = os.path.join(config['paths']['table_path'], '*.tsv')
    files = [file for file in glob.glob(pattern, recursive=True) if os.path.isfile(file)]
    for file in files:
        file_name = os.path.basename(file).split('.')[0]
        tables[file_name] = pd.read_csv(file, sep='\t', index_col=None)
    return tables

def load_texts(config):
    texts = {}
    path = config['paths']['text_path']
    documents = os.listdir(path)
    for doc in documents:
        texts[doc] = str()
        pattern = os.path.join(path , doc, '**', '*.txt')
        files = [file for file in glob.glob(pattern, recursive=True) if os.path.isfile(file)]
        for file in files:
            file_name = os.path.basename(file).split('.')[0]
            texts[doc] += open(file).read()
    return texts

def normalization(texts, tables):
    text_norm = {}
    table1 = tables['table1'].set_index('transcription')['normalisation'].to_dict()
    for doc, text in texts.items():
        # text_norm[doc] = str()
        for key, value in table1.items():
            text = text.replace(key, value)
        text_norm[doc] = text
        # text_norm[key] = text.translate(table1)
        # text_norm[key] = text.translate(str.maketrans(table1))

    return text_norm