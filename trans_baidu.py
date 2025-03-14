# ==================================
# --*-- coding: utf-8 --*--
# @Time    : 2021-08-12
# @Author  : 微信公众号：K哥爬虫
# @FileName: baidufanyi.py
# @Software: PyCharm
# ==================================

import sys
import os
import re
import execjs
import requests
from urllib import parse

from utils_lang import abbreviate_language, TranslationError

class Baidu_Translator:
    def __init__(self):
        self.session = requests.session()
        self.index_url = 'https://fanyi.baidu.com/'
        self.lang_url = 'https://fanyi.baidu.com/langdetect'
        self.basetrans_url = 'https://fanyi.baidu.com/basetrans'
        self.translate_api = 'https://fanyi.baidu.com/v2transapi'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            "Cookie":"BAIDUID=5695F9D405A926CB4C37CD9EFFFA4AD9:FG=1; BAIDUID_BFESS=5695F9D405A926CB4C37CD9EFFFA4AD9:FG=1; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1665934930,1665971726; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1665971760; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1665934930,1665971760; Hm_lpvt_afd111fa62852d1f37001d1f980b6800=1665971760; ab_sr=1.0.1_ZTJmNDE4NzBjZjc5ZjlkZDBkZTk3ZGRhYzA4YjQwNjBmNjJiMTFmMzZlMDJiMDIzNTMwNmQ2MTFkODRjZTE1NTQ4ODIzZGE1YzQ0MGM0MTc2MWFiNzRkYjdhZTc5ZjRiZDE4ZjRjNjZhZmIwNjUxMDFhMjZkZTkwMTQ4MTE0Y2VmNmRjMDMwZmY2OWYxYjdjOTg3NWEzNDgzOWRjZWRkYg=="

        }
        # self.cookies = {
        #     "BAIDUID": "624363427DBD2BFCDF0C3D6E129F5C65:FG=1"
        # }

    def get_params(self, query):
        # 获取 token 和 gtk
        self.session.get(url=self.index_url, headers=self.headers)
        # print(session.cookies.get_dict())
        response_index = self.session.get(url=self.index_url, headers=self.headers)
        token = re.findall(r"token: '([0-9a-z]+)'", response_index.text)[0]
        gtk = re.findall(r'gtk = "(.*?)"', response_index.text)[0]
        # 自动检测语言
        response_lang = self.session.post(
            url=self.lang_url, headers=self.headers, data={'query': query})
        lang = response_lang.json()['lan']
        return token, gtk, lang

    def get_sign_and_token(self, query, gtk, lang):
        def thisscript_file_dir():
            path = sys.path[0]
            if os.path.isdir(path):
                return path
            elif os.path.isfile(path):
                return os.path.dirname(path)

        with open(thisscript_file_dir() + '/baidufanyi_encrypt.js', 'r', encoding='utf-8') as f:
            baidu_js = f.read()
        sign = execjs.compile(baidu_js).call('e', query, gtk)
        translate_url = 'https://fanyi.baidu.com/#%s/en/%s' % (
            lang, parse.quote(query))
        acs_token = execjs.compile(baidu_js).call('ascToken', translate_url)
        return sign, acs_token


    def get_result(self, query, source_language, target_language, sign, token, acs_token):
        data = {
            'from': source_language,
            'to': target_language,
            'query': query,
            'transtype': 'realtime',
            'simple_means_flag': '3',
            'sign': sign,
            'token': token,
        }
        self.headers["Acs-Token"] = acs_token
        response = self.session.post(url=self.translate_api, headers=self.headers, data=data)
        _data = response.json()['trans_result']['data']
        # _dst = _data[0]['dst']
        _data_lines = [x['dst'].strip('\n')+'\n' for x in _data]
        result = _data_lines
        return result

    def translate(self, text, src_lang, dst_lang) -> str:
        source_language = abbreviate_language(src_lang, engine = 'baidu')
        target_language = abbreviate_language(dst_lang, engine = 'baidu')

        query = text
        token, gtk, lang = self.get_params(query)
        sign, acs_token = self.get_sign_and_token(query, gtk, source_language)
        result = self.get_result(query, source_language, target_language, sign, token, acs_token)
        return result


def main():
    trans = Baidu_Translator()
    query = 'power'
    src_lang = 'eng'
    dst_lang = 'chs'
    source_language = abbreviate_language(src_lang, engine = 'baidu')
    target_language = abbreviate_language(dst_lang, engine = 'baidu')

    token, gtk, lang = trans.get_params(query)
    sign, acs_token = trans.get_sign_and_token(query, gtk, source_language)
    result = trans.get_result(query, source_language, target_language, sign, token, acs_token)
    print('翻译成中文的结果为：', result)


if __name__ == '__main__':
    main()
