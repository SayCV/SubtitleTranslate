
SUPPORTED_LANGUAGES = [
    {"code": "BG", "language": "Bulgarian"},
    {"code": "ZH", "language": "Chinese"},
    {"code": "ZH", "language": "chs"},
    {"code": "CS", "language": "Czech"},
    {"code": "DA", "language": "Danish"},
    {"code": "NL", "language": "Dutch"},
    {"code": "EN", "language": "English"},
    {"code": "EN", "language": "eng"},
    {"code": "ET", "language": "Estonian"},
    {"code": "FI", "language": "Finnish"},
    {"code": "FR", "language": "French"},
    {"code": "DE", "language": "German"},
    {"code": "EL", "language": "Greek"},
    {"code": "HU", "language": "Hungarian"},
    {"code": "IT", "language": "Italian"},
    {"code": "IT", "language": "ita"},
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
