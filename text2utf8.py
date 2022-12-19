# coding:utf-8
#!/bin/env python
'''
./text2utf8.py correct_path dir
./text2utf8.py to_utf8 a.txt
'''
import os
import argparse
import chardet

def write_file(input_file, output_file):
    """写入文件"""
    content=''
    with open(input_file, 'rb') as input_opened_file:
        char_enc = chardet.detect(input_opened_file.read())['encoding']
        if char_enc == 'gb2312' or char_enc == 'gbk':
            char_enc = 'gb18030'
    print(f'Input char_enc is: {char_enc}')
    with open(input_file, 'r', encoding=char_enc, errors='ignore')as f1:
        content = f1.readlines()
    with open(output_file, 'w', encoding="utf-8")as f2:
        f2.writelines(content)

def run_text2utf8():
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
        '--verbose',
        '-v',
        action='store_true',
        help='Show the verbose output to the terminal')
    args = parser.parse_args()

    if args.output is None:
        args.output = args.input

    if args.verbose:
        print(f'Input file is: {args.input}')
        print(f'Output file is: {args.output}')
        print(f'verbose: {args.verbose}')

    write_file(args.input, args.output)

if __name__ == '__main__':
    run_text2utf8()
