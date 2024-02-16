import os
import time
import memcached_toolkit
from apscheduler.schedulers.background import BackgroundScheduler
import config


def cleanup_files():
    print('Start files cleanup')

    files = os.listdir(config.server_config['UPLOAD_DIR'])
    current_time = round(time.time())
    for file_name in files:
        metadata = memcached_toolkit.get_created_file(file_name)
        if metadata is None:
            delete_data(file_name)

        elif current_time - metadata['creation_time'] > metadata['expiration_time']:
            memcached_toolkit.remove_entry(file_name)
            delete_data(file_name)
        print(metadata)


def delete_data(file_name: str):
    file_path = os.path.join(config.server_config['UPLOAD_DIR'], file_name)
    os.remove(file_path)


def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_files, 'interval', seconds=10*60)
    print('Init Garbage Collector Scheduler')
    scheduler.start()
