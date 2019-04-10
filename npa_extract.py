from itertools import count
from string import punctuation
import com
import re
import json
import os

def find_npa(context, num):
    result=None

    rasp = re.findall(r'(?:(?:распор).+?(?:№\s?\d+.\s?-?\s?р?п?))', context)
                
    gosp = re.findall(r'(?:(?:госуд\w+\sпрограм).+?(?:»))', context)
        
    post = re.findall(r'(?:(?:постанов).+?(?:№\s?\d+))', context)
    if post:
        post = [post for post in post if not '1996' in post]

    prikaz = re.findall(r'(?:(?:приказ).+?(?:№\s?\d+))', context)

    fzn = re.findall(r'(?:(?:федер\w+\sзако).+?(?:№\s?\d+\s?-\s?фз))', context)
    if fzn:
        fzn = [fzz for fzz in fzn if not '44' in fzz]

    if rasp or gosp or post or prikaz or fzn:
        next(num)
        result = rasp+gosp+post+prikaz+fzn
        result = '\n'.join(result)

    return result

DATA = []

punctuation = punctuation.replace('.', '').replace('-', '')

in_path, out_path = com.args.in_path, com.args.out_path

num44 = count(0)
num_based = count(0)
num = count(0)

for file in os.listdir(in_path):
    idsh = re.sub(r'_\d+\.\w+', '' , file)
    filename = os.path.join(in_path, file)
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
    except:
        print(file)
        quit()
    text = re.sub(r'\s{2,}', ' ', text).replace('\n', ' ').lower()
    text = text.replace(',', '').replace('.', '').replace(u'\u2014', '-').replace(u'\u2013', '-')
    text = re.sub(r'['+punctuation+']', '', text)
    fz44surround = re.search(r'.{,700}44\s?-?\s?фз.{,700}', text)
    # result = None
    # context = None
    if fz44surround:
        context = fz44surround.group().strip()
        next(num44)
        result = find_npa(context, num)
        DATA.append([idsh, result, context])
        
    else:
        based_on = re.search(r'на основании.{,1000}', text[:int(len(text)/4)])
        if based_on:
            context = based_on.group().strip()
            next(num_based)
            result = find_npa(context, num)
            DATA.append([idsh, result, context])
    
# with open(out_path, 'r', encoding='utf-8') as f:
#     OLD_DATA = json.load(f)
# DATA_CUR = OLD_DATA+DATA

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(DATA, f)
    
print(len(DATA))
print(num44)
print(num_based)
print(num)
