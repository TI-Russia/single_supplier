import requests
import json
import time
import os
from fake_useragent import UserAgent
import re
from itertools import count
import random
from joblib import Parallel, delayed
import multiprocess
import com
import sys
import logging

def get_adrss():
    with open('proxy.txt', 'r', encoding='utf-8') as f:
        adrss = [p.strip() for p in f.readlines()]
    for a in adrss:
        yield f'http://{a}'

def main_dwnld(d, headers, p, pro_num, scan_path, Querylog):
    number = count(1)
    for z in list(zip(d['scan_url'], d['scan_name'])):

        file_link = z[0]
        file_name = z[1]

        if file_link and file_name:
            ext = re.search(r'\.[\d\w]+$', file_name).group()

            for _ in range(10):
                for _ in range(10):
                    try:
                        r = requests.get(file_link, headers=headers, proxies={'http':p})
                        break
                    except:
                        proxy = get_adrss()
                        p=next(proxy)
                NAME = f'{d["id"]}_{next(number)}{ext}'
                with open(os.path.join(scan_path, NAME), "wb") as f:
                    f.write(r.content)

                time.sleep(random.uniform(2.5, 5.5))

                next(pro_num)
                if pro_num == 30:
                    try:
                        p=next(proxy)
                    except StopIteration:
                        proxy = get_adrss()
                        p=next(proxy)
                    pro_num = count(1)

                if os.path.getsize(os.path.join(scan_path, NAME))//1024 < 5:
                    proxy = get_adrss()
                    p=next(proxy)
                else:
                    Querylog.info(f'DONE: {time.ctime()}; FILE: {NAME}')
                    break
            if os.path.getsize(os.path.join(scan_path, NAME))//1024 < 5:
                end = time.ctime()
                Querylog.info(f'END: {end}; FUCKUP REASON')
                sys.exit()

scan_path = com.args.out_path
in_path = com.args.in_path
done_files = com.args.done_path

QUERY_LOG_FORMAT = '%(name)s | %(levelname)s | %(message)s'
Querylog = logging.getLogger('querylog')
Querylog.setLevel(logging.INFO)
Filehandler = logging.FileHandler("dwnld.log")
Fileformatter = logging.Formatter(QUERY_LOG_FORMAT)
Filehandler.setFormatter(Fileformatter)
Querylog.addHandler(Filehandler)

start = time.ctime()
Querylog.info(f'START: {start}; FOR: {in_path}')

if done_files:
    done_files = os.listdir(done_files)

if not os.path.isdir(scan_path):
    os.mkdir(scan_path)

with open(in_path, 'r', encoding='utf-8') as f:
    data_clean = json.load(f)

num_cores = multiprocess.cpu_count()

ua = UserAgent()
headers = {'User-Agent': ua.random}   

data_clean_undone = []

if done_files:    
    done_files = [re.sub(r'_\d\.[\d\w]+$', '', d) for d in done_files]
    
    for d in data_clean:
        if d['scan_url'] and d['scan_name']:
            if not d['id'] in done_files:
                data_clean_undone.append(d)

pro_num = count(1)
proxy = get_adrss()
p = next(proxy)
total = len(data_clean_undone)
Querylog.info(f'TOTAL: {total}')

Parallel(n_jobs=num_cores)(delayed(main_dwnld)(d, 
                                               headers, 
                                               p, 
                                               pro_num, 
                                               scan_path, Querylog) for d in data_clean_undone)

end = time.ctime()
Querylog.info(f'END: {end}')
