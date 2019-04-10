

import multiprocess
from joblib import Parallel, delayed
import os
import argparse
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

argparser = argparse.ArgumentParser()

argparser.add_argument('--in_path', type=str)
argparser.add_argument('--out_path', type=str)

args = argparser.parse_args()

in_path, out_path = args.in_path, args.out_path


def simple_pdf_text(file, in_path, out_path):
    filename = os.path.join(in_path, file)
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    try:
        with open(filename, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()
        converter.close()
        fake_file_handle.close()
        text = text.replace('\f', ' ').replace(u'\u00AD', ' - ').strip()
        if text:
            with open(os.path.join(out_path, file.replace('.pdf', '.txt')), 'w', encoding='utf-8') as f:
                    f.write(text)
#        else:
#            cabrones.append(file)
#    except:
#        cabrones.append(file)


if not os.path.isdir(out_path):
    os.mkdir(out_path)

#cabrones = []
num_cores = multiprocess.cpu_count()
files = [f.lower() for f in os.listdir(in_path)]

Parallel(n_jobs=num_cores)(delayed(simple_pdf_text)(file, in_path, out_path) for file in files if file.endswith("_1.pdf"))

#if cabrones:
#    with open(os.path.join(out_path, "cabrones.txt")) as f:
#        f.write("\n".join(cabrones))
