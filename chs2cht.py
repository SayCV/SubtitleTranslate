from zh_langconv import *
import os
import argparse

from utils import fileopen

def simple2tradition(line):
    # 将简体转换成繁体
    line = Converter('zh-hant').convert(line.encode('utf-8').decode('utf-8'))
    line = line.encode('utf-8')
    return line


def tradition2simple(line):
    # 将繁体转换成简体
    line = Converter('zh-hans').convert(line.encode('utf-8').decode('utf-8'))
    line = line.encode('utf-8')
    return line


def TraditionalToSimplified(line):  # 繁体转简体
    line = Converter("zh-hans").convert(line)
    return line


def SimplifiedToTraditional(line):  # 简体转繁体
    line = Converter("zh-hant").convert(line)
    return line


def write_file(input_file, output_file, model='chs2cht'):
    """写入文件"""
    tmp = fileopen(input_file).decode().split('\n')
    with open(output_file, 'w', encoding='utf-8')as f2:
        # content = f1.readlines()
        for i in tmp:
            if model == 'chs2cht':
                con = ''.join(SimplifiedToTraditional(i))
            else:
                con = ''.join(TraditionalToSimplified(i))
            f2.write(con)


def run_chs2cht():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        '-i',
        dest='input',
        default='sample.chs.srt',
        help='The path to the input file')
    parser.add_argument(
        '--output',
        '-o',
        dest='output',
        help='The path to the output file')
    parser.add_argument(
        '--model',
        dest='model',
        default='chs2cht',
        help='Define the trans model: chs2cht, cht2chs')
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show the verbose output to the terminal')
    args = parser.parse_args()

    if args.output is None:
        in_file_name1, in_file_ext1 = os.path.splitext(args.input)
        in_file_name2, in_file_ext2 = os.path.splitext(in_file_name1)
        if args.model == 'chs2cht':
            out_file_lang = in_file_ext2.replace('chs', 'cht')
        else:
            out_file_lang = in_file_ext2.replace('cht', 'chs')
        args.output = in_file_name2 + out_file_lang + in_file_ext1

    if args.verbose:
        print(f'Input file is: {args.input}')
        print(f'Output file is: {args.output}')
        print(f'model: {args.model}')
        print(f'verbose: {args.verbose}')

    write_file(args.input, args.output, args.model)

if __name__ == '__main__':
    run_chs2cht()
