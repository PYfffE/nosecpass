import os
import threading
import time
import memcached_toolkit
from config import server_config


def cleanup_files(interval_seconds=600):
    while True:
        # Получаем список всех файлов в директории uploads
        files = os.listdir(server_config['UPLOAD_DIR'])
        current_time = time.time()

        for file_name in files:
            metadata = memcached_toolkit.get_created_file(file_name)
            if metadata is None:
                file_path = os.path.join(server_config['UPLOAD_DIR'], file_name)
                os.remove(file_path)

        time.sleep(interval_seconds)
