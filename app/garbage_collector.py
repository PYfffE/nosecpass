import os
import time
import memcached_toolkit
from config import server_config
from apscheduler.schedulers.background import BackgroundScheduler

def cleanup_files():
    files = os.listdir(server_config['UPLOAD_DIR'])
    current_time = time.time()

    for file_name in files:
        metadata = memcached_toolkit.get_created_file(file_name)
        if metadata is None:
            file_path = os.path.join(server_config['UPLOAD_DIR'], file_name)
            os.remove(file_path)

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(cleanup_files, 'interval', seconds=600)
    print('Start Garbage Collector Scheduler')
    scheduler.start()
    
    