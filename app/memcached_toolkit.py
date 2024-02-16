import os
import time
import uuid

from werkzeug.datastructures.file_storage import FileStorage
from pymemcache.client import base
from config import server_config
import json

memcache_host = server_config['MEMCACHED_HOST']
memcache_port = server_config['MEMCACHED_PORT']

client = base.Client((memcache_host, memcache_port))


def generate_metadata_json_string(real_filename: str, is_note: bool, expiration_time=10*60):
    return json.dumps({"real_filename": real_filename,
                       "is_note": is_note,
                       "creation_time": round(time.time()),
                       "expiration_time": expiration_time})


def generate_uuid():
    return str(uuid.uuid4())


def save_note(note_uuid, note_text):
    open(os.path.join('./uploads/' + note_uuid), 'w', encoding='utf-8').write(note_text)
    return note_uuid


def save_file(file: FileStorage, file_uuid: str):
    file.save(os.path.join('./uploads/', file_uuid))
    return file_uuid


def load_file(filename):
    pass


def create_note(uploaded_text):
    temp_uuid = generate_uuid()
    save_note(temp_uuid, uploaded_text)
    client.set(temp_uuid, generate_metadata_json_string(temp_uuid, True))
    return temp_uuid


def create_file(uploaded_file: FileStorage):
    temp_uuid = generate_uuid()
    save_file(uploaded_file, temp_uuid)
    client.set(temp_uuid, generate_metadata_json_string(uploaded_file.filename, False))
    return temp_uuid


def get_created_file(file_uuid):
    file_meta = client.get(file_uuid)
    if file_meta is None:
        return None
    json_file_meta = json.loads(file_meta.decode())

    return json_file_meta


def remove_entry(file_uuid: str):
    client.delete(file_uuid)


def delete_data(file_uuid: str):
    os.remove(os.path.join('uploads', file_uuid))


def get_keys():
    keys = client.get_sta
    return
