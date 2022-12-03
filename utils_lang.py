
SUPPORTED_LANGUAGES = [
    {"code": "BG", "language": "Bulgarian"},
    {"code": "ZH", "language": "Chinese"},
    {"code": "CS", "language": "Czech"},
    {"code": "DA", "language": "Danish"},
    {"code": "NL", "language": "Dutch"},
    {"code": "EN", "language": "English"},
    {"code": "ET", "language": "Estonian"},
    {"code": "FI", "language": "Finnish"},
    {"code": "FR", "language": "French"},
    {"code": "DE", "language": "German"},
    {"code": "EL", "language": "Greek"},
    {"code": "HU", "language": "Hungarian"},
    {"code": "IT", "language": "Italian"},
    {"code": "JA", "language": "Japanese"},
    {"code": "LV", "language": "Latvian"},
    {"code": "LT", "language": "Lithuanian"},
    {"code": "PL", "language": "Polish"},
    {"code": "PT", "language": "Portuguese"},
    {"code": "RO", "language": "Romanian"},
    {"code": "RU", "language": "Russian"},
    {"code": "SK", "language": "Slovak"},
    {"code": "SL", "language": "Slovenian"},
    {"code": "ES", "language": "Spanish"},
    {"code": "SV", "language": "Swedish"},
    # abbr
    {"code": "BG", "language": "bul"},
    {"code": "ZH", "language": "chs"},
    {"code": "CS", "language": "cze"},
    {"code": "DA", "language": "dan"},
    {"code": "NL", "language": "dut"},
    {"code": "EN", "language": "eng"},
    {"code": "ET", "language": "est"},
    {"code": "FI", "language": "fin"},
    {"code": "FR", "language": "fre"},
    {"code": "DE", "language": "ger"},
    {"code": "EL", "language": "gre"},
    {"code": "HU", "language": "hun"},
    {"code": "IT", "language": "ita"},
    {"code": "JA", "language": "jap"},
    {"code": "LV", "language": "lat"},
    {"code": "LT", "language": "lit"},
    {"code": "PL", "language": "pol"},
    {"code": "PT", "language": "por"},
    {"code": "RO", "language": "rom"},
    {"code": "RU", "language": "rus"},
    {"code": "SK", "language": "slk"},
    {"code": "SL", "language": "sln"},
    {"code": "ES", "language": "spa"},
    {"code": "SV", "language": "swe"},
]


def create_abbreviations_dictionary(languages=SUPPORTED_LANGUAGES):
    short_dict = {language["code"].lower(): language["code"]
                  for language in languages}
    verbose_dict = {
        language["language"].lower(): language["code"] for language in languages
    }
    return {**short_dict, **verbose_dict}


def abbreviate_language(language, engine = 'baidu'):
    language = language.lower()
    abbreviations = create_abbreviations_dictionary()
    if engine == 'baidu':
        return abbreviations.get(language.lower()).lower()
    else:
        return abbreviations.get(language.lower())

class TranslationError(Exception):
    def __init__(self, message):
        super(TranslationError, self).__init__(message)
