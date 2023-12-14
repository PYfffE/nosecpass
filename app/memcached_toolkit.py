import os
import uuid

from pymemcache.client import base
import json

memcache_host = '127.0.0.1'
memcache_port = 11211

client = base.Client((memcache_host, memcache_port))

# add creation and expiration time/date
def generate_metadata_json_string(real_filename: str, url_uuid: str, is_note: bool):
    return json.dumps({"real_filename": real_filename, "url_uuid": url_uuid, "is_note": is_note, "creation_date": "00:00:0000"})

def generate_uuid():
    return str(uuid.uuid4())

def save_note(filename, note_text):
    temp_uuid = generate_uuid()
    open(os.path.join('.\\uploads' + '\\' + filename), 'w', encoding='utf-8').write(note_text)
    return filename

def load_file(filename):
    pass

def create_note(uploaded_text):
    temp_uuid = generate_uuid()
    note_name = f'note_{temp_uuid}'
    save_note(temp_uuid, uploaded_text)
    client.set(temp_uuid, generate_metadata_json_string(note_name, temp_uuid, True))
    return temp_uuid

def get_created_file(file_uuid):
    file_meta = client.get(file_uuid)
    if file_meta is None:
        return None

    json_file_meta = json.loads(file_meta.decode())

    return json_file_meta

def remove_entry(file_uuid: str):
    client.delete(file_uuid)