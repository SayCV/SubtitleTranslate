# coding:utf-8
import sys
import os
import re
import codecs
import chardet
import argparse

def fileopen(input_file):
    with open(input_file, 'rb') as tmp:
        file_str = tmp.read()
        coding = chardet.detect(file_str)['encoding']
        print (coding)
        if ('UTF-16' in coding):
            tmp = file_str.decode('utf-16', 'ignore').encode('utf-8')
        elif ('GB2312' in coding or 'GBK' in coding):
            tmp = file_str.decode('gbk', 'ignore').encode('utf-8')
        elif ('Big5' in coding):
            tmp = file_str.decode('big5', 'ignore').encode('utf-8')
        elif ('UTF-8-SIG' in coding):
            tmp = file_str.decode('UTF-8-SIG', 'ignore').encode('utf-8')
        else:
            tmp = file_str.decode('utf-8', 'ignore').encode('utf-8')
    return tmp


def srt2ass(input_file, output_file):
    head_str = '''[Script Info]
; Script generated by Aegisub 9214, Daydream Cafe Edition [Shinon]
; http://www.aegisub.org/
Title: Default Aegisub file
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: no
YCbCr Matrix: None

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,sarasa-mono,26,&H00FFFFFF,&H00000000,&H00000000,&H00FF8000,0,0,0,0,100,100,0,0.00,1,2,1,2,5,5,6,134
Style: EN,DejaVu Sans Mono,16,&H006CB5DE,&HF0000000,&H80000000,&H00934A21,0,0,0,0,100,100,0,0.00,1,2,1,2,5,5,6,134
Style: 注释,微软雅黑,18,&H00FFFFFF,&HFF000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0.5,8,0,0,5,1
Style: 特效,微软雅黑,20,&H00FFFFFF,&HFF000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,5,5,5,1
Style: 歌词,方正卡通简体,14,&H00FFFFFF,&HFFFFFFFF,&H00000000,&H00000000,0,-1,0,0,100,100,0,0,1,1,0,1,25,5,43,1
Style: 歌词原文,方正卡通简体,14,&H00146EB3,&HFFFFFFFF,&H00000000,&H00000000,0,-1,0,0,100,100,0,0,1,1,0,1,25,5,43,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
    
    tmp = fileopen(input_file).decode()

    tmp = tmp + '\r\n\r\n'
    tmp = tmp.replace('{', '')
    tmp = tmp.replace('}', '')

    # match timestamp: `00:00:06,000` -> 00:00:06.000
    pattern = re.compile(r'(\d{1,2}:\d{1,2}:\d{1,2}),(\d{1,3})')
    tmp = pattern.sub(r'\1.\2', tmp)

    # remove blank line: `00:00:06.000 --> 00:00:58.101`
    pattern = re.compile(r'(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3} ?--> ?\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n\r\n')
    tmp = pattern.sub(r'\1\r\n', tmp)

    # match dialogue: `\an1\pos(...)`
    pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(\\an\d\\pos\(.+\))')
    tmp = pattern.sub(r'Dialogue: 0,\1,\2,注释,,0,0,0,,{\3\\fad(500,500)\\fs20}', tmp)

    # match dialogue: `\pos(...)`
    pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(\\pos\(.+\))')
    tmp = pattern.sub(r'Dialogue: 0,\1,\2,注释,,0,0,0,,{\3\\fad(500,500)\\fs20}', tmp)

    # match dialogue: `\an1`
    pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(\\an\d)')
    tmp = pattern.sub(r'Dialogue: 0,\1,\2,注释,,0,0,0,,{\3\\fad(500,500)\\fs20}', tmp)

    # match dialogue: `双行`
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{42,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs08}\3\\N{\\rEN}\4 ', tmp)
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{40,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs10}\3\\N{\\rEN}\4 ', tmp)
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{38,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs11}\3\\N{\\rEN}\4 ', tmp)
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{36,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs12}\3\\N{\\rEN}\4 ', tmp)
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{34,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs13}\3\\N{\\rEN}\4 ', tmp)
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{32,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs14}\3\\N{\\rEN}\4 ', tmp)
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{30,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs15}\3\\N{\\rEN}\4 ', tmp)
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{28,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs16}\3\\N{\\rEN}\4 ', tmp)
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{26,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs18}\3\\N{\\rEN}\4 ', tmp)
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{24,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs20}\3\\N{\\rEN}\4 ', tmp)
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{22,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs22}\3\\N{\\rEN}\4 ', tmp)
    ## pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.{20,})\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    ## tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,{\\fs24}\3\\N{\\rEN}\4 ', tmp)

    pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.+)\r\n([ …!\w\.,?\'\"-:;\[\]\(\)%$@&*\^+~<>]+)\r\n')
    tmp = pattern.sub(lambda x: auto_counts_sub(x), tmp)

    # match dialogue: `单行`
    pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.+)\r\n\r\n')
    tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,\3\n', tmp)

    # match timestamp: `00:00:06,000` -> 00:00:06.00
    pattern = re.compile(r'(\d{1,2}:\d{1,2}:\d{1,2}\.\d{2})\d')
    tmp = pattern.sub(r'\1', tmp)

    pattern = re.compile(r'\n')
    tmp = pattern.sub(r'\r\n', tmp)
    pattern = re.compile(r'\r\r\n')
    tmp = pattern.sub(r'\r\n', tmp)

    # remove blank dialogue
    pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n\r\n\r\n')
    tmp = pattern.sub(r'', tmp)

    # match song: ``
    pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.+)\r\n(.*♪.*♪.*)\r\n')
    tmp = pattern.sub(r'Dialogue: 0,\1,\2,歌词,,0,0,0,,\3\\N{\\r歌词原文}\4', tmp)
    pattern = re.compile(r'\d{1,4}\r\n(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3}) ?--> ?(\d{1,2}:\d{1,2}:\d{1,2}\.\d{1,3})\r\n(.+)\r\n(.+)\r\n')
    tmp = pattern.sub(r'Dialogue: 0,\1,\2,Default,,0,0,0,,\3\\N{\\rEN}\4', tmp)

    tmp = tmp.replace('\r\n', '\\N')
    tmp = re.sub(r'(\\N){1,8}', r'\\N', tmp)
    tmp = re.sub(r'(\\N){1,8}$', '', tmp)
    tmp = tmp.replace('\\NDialogue:', '\r\nDialogue:')

    output_str = head_str + '\n' + tmp.strip(' ')
    # print output_str.decode('utf-8')
    
    with open(output_file + '.ass', 'wb') as output:
        # output.write(codecs.BOM_UTF16_LE)
        # output.write(unicode(output_str, 'utf-8').encode('utf-16-le'))
        output.write(codecs.BOM_UTF8)
        output.write(output_str.encode('utf-8'))

def auto_counts_sub(value):
    str1 = value.group(1)
    str2 = value.group(2)
    str3 = value.group(3)
    str4 = value.group(4)
    #print(3, value.group(3), len(value.group(3).encode('utf-8')))
    #print(3, value.group(3), len(value.group(3)))
    str3_size = 0
    str3_len = len(str3.encode('utf-8'))
    ret = ''
    if str3_len >= 3*30:
        gap: int = (str3_len/3 - 30)/2
        str3_size = 15 - 1*gap
        ret = r'Dialogue: 0,%s,%s,Default,,0,0,0,,{\fs%d}%s\N{\rEN}%s ' % (str1, str2, str3_size, str3, str4)
    elif str3_len >= 3*20:
        gap: int = (str3_len/3 - 21)/2
        str3_size = 24 - 2*gap
        ret = r'Dialogue: 0,%s,%s,Default,,0,0,0,,{\fs%d}%s\N{\rEN}%s ' % (str1, str2, str3_size, str3, str4)
    else:
        ret = r'Dialogue: 0,%s,%s,Default,,0,0,0,,%s\N{\rEN}%s ' % (str1, str2, str3, str4)
    return ret

if __name__ == '__main__':
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
        '--verbose',
        '-v',
        action='store_true',
        help='Show the verbose output to the terminal')
    args = parser.parse_args()

    # input_file = sys.argv[1]
    input_file = args.input
    output_file = args.output
    if args.output is None:
        output_file = '.'.join(input_file.split('.')[:-1])

    srt2ass(input_file, output_file)
