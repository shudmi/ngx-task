import os
import random
import string
import zipfile
from xml.etree import cElementTree as ET
from uuid import uuid4


def make_name(count=20):
    return ''.join(random.sample(string.ascii_letters, count))


def generate_document():
    root = ET.Element('root')
    id_element = ET.Element('var', {'name': 'id', 'value': str(uuid4())})
    level_element = ET.Element('var', {'name': 'level', 'value': str(random.randint(1, 100))})

    objects = ET.Element('objects')
    objects.extend(ET.Element('object', {'name': make_name()})
                   for _ in range(random.randint(1, 10)))

    root.extend((id_element, level_element, objects))
    return root


def create_archive(filename, documents_count=100):
    with zipfile.ZipFile(filename, 'w') as zf:
        for doc_number in range(1, documents_count + 1):
            document_name = 'document-{}.xml'.format(doc_number)
            tree = ET.ElementTree(generate_document())
            try:
                tree.write(document_name, encoding='utf-8')
                zf.write(document_name)
            finally:
                if os.path.exists(document_name):
                    os.remove(document_name)
