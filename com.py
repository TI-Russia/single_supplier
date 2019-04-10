import argparse

argparser = argparse.ArgumentParser()

argparser.add_argument('--in_path', type=str)
argparser.add_argument('--out_path', type=str)
argparser.add_argument('--mode', type=str)
argparser.add_argument('--done_path', type=str, default='')

args = argparser.parse_args()
