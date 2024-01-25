import glob
import os
import pandas as pd
import re

def load_tables(config):
    tables = {}
    pattern = os.path.join(config['paths']['table_path'], '*.tsv')
    files = [file for file in glob.glob(pattern, recursive=True) if os.path.isfile(file)]
    for file in files:
        file_name = os.path.basename(file).split('.')[0]
        tables[file_name] = pd.read_csv(file, sep='\t', escapechar='\\', index_col=None)
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

def norm_table1(texts, tables):
    text_norm = {}
    table = tables['table1'].set_index('transcription')['normalisation'].to_dict()
    for doc, text in texts.items():
        for key, value in table.items():
            text = text.replace(key, value)
        text_norm[doc] = text

    return text_norm

def norm_table2(texts, tables):
    text_norm = {}
    table = tables['table2'].set_index('transcription')['normalisation'].to_dict()
    for doc, text in texts.items():
        for key, value in table.items():
            text = re.sub(key, value, text)
        text_norm[doc] = text

    return text_norm

def norm_table3(texts, tables):
    text_norm = {}
    table = {}
    for index, row in tables['table3'].iterrows():
        table[row['transcription']] = (row['normalisation'], row['exception'])
    for doc, text in texts.items():
        text_norm[doc] = str()
        for key, value in table.items():
            exception = re.compile(value[1])
            for i in range(len(text)):
                if text[i] == key:
                    if bool(exception.search(text[i-1])) or bool(exception.search(text[i+1])):
                        text_norm[doc] += text[i]
                    else:
                        text_norm[doc] += value[0]
                else:
                    text_norm[doc] += text[i]

    return text_norm

def normalisation(texts, tables):

    # normalisation by table1
    text_norm1 = norm_table1(texts, tables)

    # normalisation by table2
    text_norm2 = norm_table2(text_norm1, tables)

    # normalisation by table3
    text_norm = norm_table3(text_norm2, tables)

    return text_norm

def export_text(config, text_norm):
    for key, value in text_norm.items():
        output_path = config['paths']['output_path'] + key + '.txt'
        with open(output_path, 'w') as file:
            file.write(value)