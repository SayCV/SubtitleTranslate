from utils import translate_and_compose

import os
import argparse


def run_translate_ex1():

    input_file = "sample.en.srt"

    # Translate the subtitle into Chinese, save both English and Chinese to the output srt file
    # translate_and_compose(input_file, output_file, src_lang, target_lang, encoding='UTF-8', mode='split', both=True, space=False)
    translate_and_compose(input_file, 'sample_en_cn_both.srt', 'en', 'zh-CN')
    # translate_and_compose(input_file, 'sample_en_cn_both.srt', 'en', 'zh-CN', encoding='UTF-8-sig')

    # Translate the subtitle into Chinese, save only Chinese subtitle to the output srt file
    translate_and_compose(input_file, 'sample_cn_only.srt',
                          'en', 'zh-CN', both=False)

    # Translate the subtitle into German, save both English and German to the output srt file
    # In German language, each words separated by space, so space=True
    translate_and_compose(
        input_file, 'sample_en_de_both.srt', 'en', 'de', space=True)

    # Translate the subtitle into Japanese, save both English and Japanese to the output srt file
    # In Japanese(Chinese, Korean), words are characters which are NOT separated by space, so space=False (default)
    translate_and_compose(input_file, 'sample_en_ja_both.srt', 'en', 'ja')


def run_translate():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        '-i',
        dest='input',
        default='sample.en.srt',
        help='The path to the input file')
    parser.add_argument(
        '--output',
        '-o',
        dest='output',
        help='The path to the output file')
    parser.add_argument(
        '--src',
        dest='src',
        default='eng',
        help='Define the source subtitle language')
    parser.add_argument(
        '--dst',
        dest='dst',
        default='chs',
        help='Define the target subtitle language')
    parser.add_argument(
        '--encoding',
        dest='encoding',
        default='UTF-8',
        help='Define the source file encoding')
    parser.add_argument(
        '--engine',
        dest='engine',
        default='youdao',
        help='Define the trans engine: baidu, google, bing')
    parser.add_argument(
        '--model',
        dest='model',
        default='naive',
        help='Define the trans model: naive, split')
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show the verbose output to the terminal')
    parser.add_argument(
        '--both',
        action='store_false',
        help='both')
    parser.add_argument(
        '--space',
        action='store_true',
        help='space')
    args = parser.parse_args()

    output_file2 = ''
    if args.output is None:
        in_file_name1, in_file_ext1 = os.path.splitext(args.input)
        in_file_name2, in_file_ext2 = os.path.splitext(in_file_name1)
        out_file_lang = args.dst
        args.output = in_file_name2 + '.' + out_file_lang + in_file_ext1
        out_file_lang = args.dst + '+' + args.src
        output_file2 = in_file_name2 + '.' + out_file_lang + in_file_ext1

    if args.verbose:
        print(f'Input file is: {args.input}')
        print(f'Output file is: {args.output}')
        print(f'both: {args.both}')
        print(f'space: {args.space}')
        print(f'engine: {args.engine}')
        print(f'encoding: {args.encoding}')
        print(f'model: {args.model}')
        print(f'verbose: {args.verbose}')

    input_file = args.input
    output_file = args.output
    src_lang = args.src
    dst_lang = args.dst

    translate_and_compose(input_file, output_file, output_file2, src_lang,
                          dst_lang, engine=args.engine, encoding=args.encoding, mode=args.model, both=args.both)


if __name__ == '__main__':
    # run_translate_ex1()
    run_translate()
