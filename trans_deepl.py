import translators as ts

from utils_lang import abbreviate_language, TranslationError

class Deepl_Translator:
    def __init__(self):
        pass

    def translate(self, text, src_lang, dst_lang) -> str:
        source_language = abbreviate_language(src_lang, engine = 'baidu')
        target_language = abbreviate_language(dst_lang, engine = 'baidu')

        result = ts.deepl(text, from_language = source_language, to_language = target_language)
        return result


def main():
    trans = Deepl_Translator()
    query = 'power'
    src_lang = 'eng'
    dst_lang = 'chs'
    source_language = abbreviate_language(src_lang, engine = 'baidu')
    target_language = abbreviate_language(dst_lang, engine = 'baidu')

    result = trans.translate(query, src_lang, dst_lang)
    print('翻译成中文的结果为：', result)


if __name__ == '__main__':
    main()
