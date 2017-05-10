import os
import random
import string
import zipfile
from xml.etree import cElementTree as ET
from uuid import uuid4

from ngx_task import settings


def make_name(count=settings.OBJECT_NAME_LENGTH):
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


def archive_documents(filename, count=settings.ARCHIVE_DOCUMENTS_COUNT):
    arc_filename = os.path.join(settings.DATA_DIR, filename)
    with zipfile.ZipFile(arc_filename, 'w') as zf:
        for doc_number in range(1, count + 1):
            document_name = '{}-document-{}.xml'.format(filename, doc_number)
            zf.write(document_name, ET.tostring(generate_document(), encoding='utf-8'))


def process_archive(path, f_queue, obj_queue):
    with zipfile.ZipFile(path, 'r') as zf:
        for member in zf.namelist():
            xml_data = ET.fromstring(zf.read(member).decode('utf-8'))
            file_id = xml_data.find('var[@name="id"]').get('value')
            file_level = xml_data.find('var[@name="level"]').get('value')

            f_queue.put((file_id, file_level))
            for obj in xml_data.iterfind('objects/object'):
                obj_queue.put((file_id, obj.get('name')))
