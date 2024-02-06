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
        table[row['transcription']] = (row['normalisation'], row['exception'], row['exc_len'])
    for doc, text in texts.items():
        text_list = list(text)
        for key, value in table.items():
            exception = re.compile(value[1])
            exc_len = value[2]
            for i in range(len(text_list)):
                pos_end = i + len(key)
                start = 0 if i - exc_len <= 0 else i - exc_len
                end = len(text_list) -1 if pos_end + exc_len > len(text_list) else pos_end + exc_len
                str_range = ''.join(text_list[start:end])
                if len(key) > 1:
                    if text_list[i:pos_end] == list(key):
                        if not bool(exception.search(str_range)):
                            text_list[i:pos_end] = [value[0]] + [''] * (pos_end - i - 1)
                else:
                    if text_list[i] == key:
                        if not bool(exception.search(str_range)):
                            text_list[i] = value[0]

        text_norm[doc] = ''.join(text_list)

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