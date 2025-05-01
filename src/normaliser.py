import re

class Normaliser:
    def __init__(self, texts, tables):
        self.texts = texts
        self.tables = tables

    def norm_abbreviation(self):
        text_norm = {}
        table = self.tables['abbreviations'].set_index('transcription')['normalisation'].to_dict()
        for file, text in self.texts.items():
            if not isinstance(text, str):
                continue
            for key, value in table.items():
                text = text.replace(key, value)
            text_norm[file] = text

        return text_norm

    def norm_table1(self, texts):
        text_norm = {}
        table = self.tables['table1'].set_index('transcription')['normalisation'].to_dict()
        for file, text in texts.items():
            for key, value in table.items():
                text = text.replace(key, value)
            text_norm[file] = text

        return text_norm

    def norm_table2(self, texts):
        text_norm = {}
        table = self.tables['table2'].set_index('transcription')['normalisation'].to_dict()
        for file, text in texts.items():
            for key, value in table.items():
                text = re.sub(key, value, text)
            text_norm[file] = text

        return text_norm

    def norm_table3(self, texts):
        text_norm = {}
        table = {}
        for index, row in self.tables['table3'].iterrows():
            table[row['transcription']] = {'norm': row['normalisation'], 'exc': row['exception'],
                                           'exc_len': row['exc_len'], 'scope': row['scope']}
        for file, text in texts.items():
            text_list = list(text)
            for key, value in table.items():
                exception, exc_len, scope = re.compile(value['exc']), value['exc_len'], value['scope']
                for i in range(len(text_list)):
                    pos_end = i + len(key)
                    start = 0 if i - exc_len <= 0 else i - exc_len
                    end = len(text_list) - 1 if pos_end + exc_len > len(text_list) else pos_end + exc_len
                    if scope == 'left':
                        str_range = ''.join(text_list[start:i])
                    elif scope == 'right':
                        str_range = ''.join(text_list[i + 1:end])
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

            text_norm[file] = ''.join(text_list)

        return text_norm

    def normalisation(self):
        # normalisation by abbreviations
        print("Processing normalisation using the abbreviation table ...")
        text_abbreviation = self.norm_abbreviation()

        # normalisation by table1
        print("Processing normalisation using table1 ...")
        text_norm1 = self.norm_table1(text_abbreviation)

        # normalisation by table2
        print("Processing normalisation using table2 ...")
        text_norm2 = self.norm_table2(text_norm1)

        # normalisation by table3
        print("Processing normalisation using table3 ...")
        text_norm = self.norm_table3(text_norm2)

        return text_norm