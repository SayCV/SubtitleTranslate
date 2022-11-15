import translators as ts

from utils_lang import abbreviate_language, TranslationError

class Youdao_Translator:
    def __init__(self):
        pass

    def translate(self, text, src_lang, dst_lang) -> str:
        source_language = abbreviate_language(src_lang, engine = 'baidu')
        target_language = abbreviate_language(dst_lang, engine = 'baidu')

        result = ts.youdao(text, from_language = source_language, to_language = target_language)
        return result

class TranslateCom_Translator:
    def __init__(self):
        pass

    def translate(self, text, src_lang, dst_lang) -> str:
        source_language = abbreviate_language(src_lang, engine = 'baidu')
        target_language = abbreviate_language(dst_lang, engine = 'baidu')

        result = ts.translateCom(text, from_language = source_language, to_language = target_language)
        return result

class Utibet_Translator:
    def __init__(self):
        pass

    def translate(self, text, src_lang, dst_lang) -> str:
        source_language = abbreviate_language(src_lang, engine = 'baidu')
        target_language = abbreviate_language(dst_lang, engine = 'baidu')

        result = ts.utibet(text, from_language = source_language, to_language = target_language)
        return result

class Papago_Translator:
    def __init__(self):
        pass

    def translate(self, text, src_lang, dst_lang) -> str:
        source_language = abbreviate_language(src_lang, engine = 'baidu')
        target_language = abbreviate_language(dst_lang, engine = 'baidu')

        result = ts.papago(text, from_language = source_language, to_language = target_language)
        return result

class Lingvanex_Translator:
    def __init__(self):
        pass

    def translate(self, text, src_lang, dst_lang) -> str:
        source_language = abbreviate_language(src_lang, engine = 'baidu')
        target_language = abbreviate_language(dst_lang, engine = 'baidu')

        result = ts.lingvanex(text, from_language = source_language, to_language = target_language)
        return result


def main():
    trans = Youdao_Translator()
    query = 'power'
    src_lang = 'eng'
    dst_lang = 'chs'
    source_language = abbreviate_language(src_lang, engine = 'baidu')
    target_language = abbreviate_language(dst_lang, engine = 'baidu')

    result = trans.translate(query, src_lang, dst_lang)
    print('翻译成中文的结果为：', result)


if __name__ == '__main__':
    main()
