import glob
import os
import pandas as pd

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
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            if file.lower().endswith('.txt'):
                full_path = os.path.join(dirpath, file)
                texts[file] = open(full_path).read()
    return texts

def export_text(config, text_norm):
    output_dir = config['paths']['output_path']
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    for file, text in text_norm.items():
        filename = os.path.basename(file)
        output_path = output_dir + filename
        with open(output_path, 'w') as file:
            file.write(text)