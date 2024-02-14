import glob
import os
import pandas as pd
import re

def load_tables(config):
    tables = {}
    pattern = os.path.join(config['paths']['table_path'], '*.tsv')
    flag = int(config['parameters']['flag'])
    files = [file for file in glob.glob(pattern, recursive=True) if os.path.isfile(file)]
    flag_tables = ['abbreviations', 'table3']
    for file in files:
        file_name = os.path.basename(file).split('.')[0]
        df = pd.read_csv(file, sep='\t', escapechar='\\', index_col=None)
        if file_name in flag_tables:
            df['flag'] = df['flag'].apply(pd.to_numeric, errors='coerce').astype('Int64')
            tables[file_name] = df[df['flag'] == flag]
        else:
            tables[file_name] = df

    return tables

def load_texts(config):
    texts = {}
    path = config['paths']['text_path']
    documents = os.listdir(path)
    for doc in documents:
        texts[doc] = {}
        pattern = os.path.join(path , doc, '**', '*.txt')
        files = [file for file in glob.glob(pattern, recursive=True) if os.path.isfile(file)]
        for file in files:
            file_name = os.path.basename(file).split('.')[0]
            texts[doc][file_name] = open(file).read()
    return texts

def norm_abbreviation(texts, tables):
    text_norm = {}
    table = tables['abbreviations'].set_index('transcription')['normalisation'].to_dict()
    for doc in texts.keys():
        text_norm[doc] = {}
        for file_name, text in texts[doc].items():
            for key, value in table.items():
                text = text.replace(key, value)
            text_norm[doc][file_name] = text

    return text_norm

def norm_table1(texts, tables):
    text_norm = {}
    table = tables['table1'].set_index('transcription')['normalisation'].to_dict()
    for doc in texts.keys():
        text_norm[doc] = {}
        for file_name, text in texts[doc].items():
            for key, value in table.items():
                text = text.replace(key, value)
            text_norm[doc][file_name] = text

    return text_norm

def norm_table2(texts, tables):
    text_norm = {}
    table = tables['table2'].set_index('transcription')['normalisation'].to_dict()
    for doc in texts.keys():
        text_norm[doc] = {}
        for file_name, text in texts[doc].items():
            for key, value in table.items():
                text = re.sub(key, value, text)
            text_norm[doc][file_name] = text

    return text_norm

def norm_table3(texts, tables):
    text_norm = {}
    table = {}
    for index, row in tables['table3'].iterrows():
        table[row['transcription']] = {'norm': row['normalisation'], 'exc': row['exception'], 'exc_len': row['exc_len'], 'scope': row['scope']}
    for doc in texts.keys():
        text_norm[doc] = {}
        for file_name, text in texts[doc].items():
            text_list = list(text)
            for key, value in table.items():
                exception = re.compile(value['exc'])
                exc_len = value['exc_len']
                scope = value['scope']
                for i in range(len(text_list)):
                    pos_end = i + len(key)
                    start = 0 if i - exc_len <= 0 else i - exc_len
                    end = len(text_list) -1 if pos_end + exc_len > len(text_list) else pos_end + exc_len
                    if scope == 'left':
                        str_range = ''.join(text_list[start:i])
                    elif scope == 'right':
                        str_range = ''.join(text_list[i+1:end])
                    elif scope == 'both':
                        str_range = ''.join(text_list[start:end])
                    else:
                        print('The entry of scope e in table3 is not proper.')
                    if i - exc_len <= 0 or pos_end + exc_len > len(text_list):
                        str_range = ''
                    if len(key) > 1:
                        if text_list[i:pos_end] == list(key):
                            if not bool(exception.search(str_range)):
                                text_list[i:pos_end] = [value['norm']] + [''] * (pos_end - i - 1)
                    else:
                        if text_list[i] == key:
                            if not bool(exception.search(str_range)):
                                text_list[i] = value['norm']

            text_norm[doc][file_name] = ''.join(text_list)

    return text_norm

def normalisation(texts, tables):

    # normalisation by abbreviations
    text_abbreviation = norm_abbreviation(texts, tables)

    # normalisation by table1
    text_norm1 = norm_table1(text_abbreviation, tables)

    # normalisation by table2
    text_norm2 = norm_table2(text_norm1, tables)

    # normalisation by table3
    text_norm = norm_table3(text_norm2, tables)

    return text_norm

def export_text(config, text_norm):
    for doc in text_norm.keys():
        output_dir = config['paths']['output_path'] + doc + '/'
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        for key, value in text_norm[doc].items():
            output_path = output_dir + key + '.txt'
            with open(output_path, 'w') as file:
                file.write(value)