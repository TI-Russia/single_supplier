import multiprocess
from joblib import Parallel, delayed
import os
import com
import textract
import time
import logging

def extract(file, in_path, out_path, mode, Querylog):
    filename = os.path.join(in_path, file)
    try:
        text = textract.process(filename, method='tesseract', language='rus')
        with open(os.path.join(out_path, file.replace(f'.{mode}', '.txt')), 'wb') as f:
            f.write(text)
    except:
        Querylog.info(f'CANT READ: {file}')
        pass

in_path, out_path, mode = com.args.in_path, com.args.out_path, com.args.mode

QUERY_LOG_FORMAT = '%(name)s | %(levelname)s | %(message)s'
Querylog = logging.getLogger('querylog')
Querylog.setLevel(logging.INFO)
Filehandler = logging.FileHandler("query.log")
Fileformatter = logging.Formatter(QUERY_LOG_FORMAT)
Filehandler.setFormatter(Fileformatter)
Querylog.addHandler(Filehandler)

start = time.ctime()
Querylog.info(f'START: {start}; WITH MODE: {mode}')

if not os.path.isdir(out_path):
    os.mkdir(out_path)

start_done_num = len(os.listdir(out_path))

num_cores = multiprocess.cpu_count()

all_files = [f.lower() for f in os.listdir(in_path)]
files = [f for f in all_files if not f.replace(f'.{mode}', '.txt') in os.listdir(out_path)]
Querylog.info(f'NUMBER OF FILES: {len(files)}')

if files:
    Parallel(n_jobs=num_cores)(delayed(extract)(file, in_path, out_path, mode, Querylog) 
    	for file in files if file.endswith(f'.{mode}'))

end = time.ctime()
Querylog.info(f'END: {end}')
Querylog.info(f'RESULT: {len(os.listdir(out_path))-start_done_num}')