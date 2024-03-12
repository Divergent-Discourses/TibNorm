import os
from xml.etree import ElementTree as ET
import fnmatch
import pandas as pd

class XMLParagraphExtractor:
    
    def __init__(self, namespaces={'ns': 'http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15'}):
        self.namespaces = namespaces

    def parse_filename(self, fstring):

        fstring_elements = fstring.split('/')

        f_attributes = fstring_elements[3].split()
        f_index = f_attributes[0][:4]

        return {'filename':fstring, 'doc_index':f_index}

    def extract_xml(self, fname):

        file_metadata = self.parse_filename(fname)

        with open(fname, 'r') as f:
            data = f.read()

        root = ET.fromstring(data)
        content_keys = ['paragraph', 'paragraph_idx', 'filename', 'doc_index']
        contents = {k: [] for k in content_keys}
        
        region_idx = 0
        
        for text_region in root.findall('.//ns:TextRegion', self.namespaces):
            region_text = ''
            for text_equiv in text_region.findall('.//ns:TextEquiv/ns:Unicode', self.namespaces):
                content = text_equiv.text

                if content:
                    region_text = region_text + content
                    region_text = region_text.replace('\n', '')
                    region_text = region_text.replace('\t', ' ')

            contents['paragraph'].append(region_text)
            contents['paragraph_idx'].append(region_idx)
            for k in file_metadata.keys():
                contents[k].append(file_metadata[k])

            region_idx += 1
            
        return pd.DataFrame(contents)
        

    def parse_transkribus(self, path):

        xml_files = []
        excluded_files = ['mets.xml', 'metadata.xml']
        
        if os.path.isfile(path) and path.endswith('.xml') and os.path.basename(path) not in excluded_files:
            xml_files.append(path)
        
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if not fnmatch.fnmatch(d, '*.zip') and not fnmatch.fnmatch(d, '*.pdf')]

                for file in files:
                    if file.endswith('.xml') and file not in ['mets.xml', 'metadata.xml']:
                        xml_files.append(os.path.join(root, file))
        
        else:
            print('input is neither a directory nor an xml file')
            return

        for fname in xml_files:
            
            try:
                data = self.extract_xml(fname)
                csv_filename = fname.rsplit('.', 1)[0] + '.csv'
                data.to_csv(csv_filename)
                print(f'Processed and saved: {csv_filename}')
                
            except Exception as e:
                print(f'Error processing {fname}: {e}')