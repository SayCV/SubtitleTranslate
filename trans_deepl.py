
import sys
import os
import re
import execjs
import json
import requests
from urllib import parse
import time
from random import randrange

from utils_lang import abbreviate_language, TranslationError

class Deepl_Translator:
    API_URL = "https://www2.deepl.com/jsonrpc"

    MAGIC_NUMBER = int("CAFEBABE", 16)

    SUPPORTED_FORMALITY_TONES = ["formal", "informal"]

    def __init__(self):
        self.session = requests.session()
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US;q=0.8,en;q=0.7",
            "authority": "www2.deepl.com",
            "content-type": "application/json",
            "origin": "https://www.deepl.com",
            "referer": "https://www.deepl.com/translator",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": (
                "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/83.0.4103.97 Mobile Safari/537.36"
            ),
        }

    def calculate_valid_timestamp(timestamp, i_count):
        try:
            return timestamp + (i_count - timestamp % i_count)
        except ZeroDivisionError:
            return timestamp

    def generate_timestamp(sentences):
        now = int(time.time() * 1000)
        i_count = 1
        for sentence in sentences:
            i_count += sentence.count("i")

        return Deepl_Translator.calculate_valid_timestamp(now, i_count)

    def generate_id():
        return randrange(1_000_000, 100_000_000)

    def generate_split_sentences_request_data(text, identifier=MAGIC_NUMBER, **kwargs):
        return {
            "jsonrpc": "2.0",
            "method": "LMT_split_into_sentences",
            "params": {
                "texts": [text],
                "lang": {"lang_user_selected": "auto", "user_preferred_langs": []},
            },
            "id": identifier,
        }

    def generate_jobs(sentences, beams=1):
        jobs = []
        for idx, sentence in enumerate(sentences):
            job = {
                "kind": "default",
                "raw_en_sentence": sentence,
                "raw_en_context_before": sentences[:idx],
                "raw_en_context_after": [sentences[idx + 1]]
                if idx + 1 < len(sentences)
                else [],
                "preferred_num_beams": beams,
            }
            jobs.append(job)
        return jobs

    def generate_common_job_params(formality_tone):
        if not formality_tone:
            return {}
        if formality_tone not in Deepl_Translator.SUPPORTED_FORMALITY_TONES:
            raise ValueError(
                f"Formality tone '{formality_tone}' not supported.")
        return {"formality": formality_tone}

    def generate_translation_request_data(
        source_language,
        target_language,
        sentences,
        identifier=MAGIC_NUMBER,
        alternatives=1,
        formality_tone=None,
    ):
        return {
            "jsonrpc": "2.0",
            "method": "LMT_handle_jobs",
            "params": {
                "jobs": Deepl_Translator.generate_jobs(sentences, beams=alternatives),
                "lang": {
                    "user_preferred_langs": [target_language, source_language],
                    "source_lang_computed": source_language,
                    "target_lang": target_language,
                },
                "priority": 1,
                "commonJobParams": Deepl_Translator.generate_common_job_params(formality_tone),
                "timestamp": Deepl_Translator.generate_timestamp(sentences),
            },
            "id": identifier,
        }

    def extract_translated_sentences(json_response):
        if 'result' not in json_response:
            raise TranslationError('DeepL call resulted in a unknown result.')

        translations = json_response["result"]["translations"]
        translated_sentences = [
            translation["beams"][0]["postprocessed_sentence"]
            for translation in translations
        ]
        return translated_sentences

    def extract_split_sentences(json_response):
        if 'result' not in json_response:
            raise TranslationError('DeepL call resulted in a unknown result.')

        return json_response["result"]["splitted_texts"][0]

    def split_into_sentences(self, text, **kwargs):
        data = Deepl_Translator.generate_split_sentences_request_data(text, **kwargs)
        
        time.sleep(int(1))
        response = requests.post(Deepl_Translator.API_URL, data=json.dumps(data), headers=self.headers)
        if response.status_code == 429:
            time.sleep(int(1))
            response.raise_for_status()

        json_response = response.json()
        sentences = Deepl_Translator.extract_split_sentences(json_response)

        return sentences


    def request_translation(self, source_language, target_language, text, **kwargs):
        sentences = self.split_into_sentences(text, **kwargs)
        data = Deepl_Translator.generate_translation_request_data(
            source_language, target_language, sentences, **kwargs
        )
        response = requests.post(Deepl_Translator.API_URL, data=json.dumps(data), headers=self.headers)
        return response

    def translate(self, text, src_lang, dst_lang) -> str:
        source_language = abbreviate_language(src_lang)
        target_language = abbreviate_language(dst_lang)

        time.sleep(int(1))
        response = self.request_translation(source_language, target_language, text)
        if response.status_code == 429:
            time.sleep(int(1))
            response.raise_for_status()

        json_response = response.json()
        translated_sentences = Deepl_Translator.extract_translated_sentences(json_response)
        translated_text = " ".join(translated_sentences)

        return translated_text


def main():
    trans = Deepl_Translator()
    text = 'power'
    source_language = "eng"
    target_language = "chs"
    result = trans.translate(text, source_language, target_language)
    print('翻译成中文的结果为：', result)


if __name__ == '__main__':
    main()
