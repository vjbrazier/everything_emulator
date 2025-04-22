import paths
import atexit
from datetime import datetime
from pathlib import Path

log = []

def get_time():
    return datetime.now().strftime("%I:%M:%S %p")

def add_to_log(message):
    print(f'{get_time()}: {message}')
    log.append(f'{get_time()}: {message}')

def count_logs():
    folder_path = Path(paths.log_path)
    file_count = sum(1 for f in folder_path.iterdir() if f.is_file())

    return file_count

def write_log():
    file_count = count_logs()
    log_filename = Path(paths.log_path) / f'log_{file_count + 1}.txt'

    with open(log_filename, 'w') as f:       
        for line in log:
            f.write(line + '\n')

atexit.register(write_log)