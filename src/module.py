import glob
import os
import pandas as pd

def load_tables(config):
    tables = {}
    pattern = os.path.join(config['paths']['table_path'], '*.tsv')
    files = [file for file in glob.glob(pattern, recursive=True) if os.path.isfile(file)]
    for file in files:
        file_name = os.path.basename(file).split('.')[0]
        tables[file_name] = pd.read_csv(file, sep='\t')
    return tables

def load_texts(config):
    texts = {}
    pattern = os.path.join(config['paths']['text_path'], '**', '*.txt')
    files = [file for file in glob.glob(pattern, recursive=True) if os.path.isfile(file)]
    for file in files:
        file_name = os.path.basename(file).split('.')[0]
        texts[file_name] = open(file).read()
    return texts

def normalization(config, tables):
    table = tables['table1']


    # re.sub(r'\)',r'',line)