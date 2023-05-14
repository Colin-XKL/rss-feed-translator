import logging
from functools import lru_cache


# TODO more translation backend
# maybe paddle nlp
@lru_cache(maxsize=128, typed=True)
def translate_html(input_html, translator_name="aliyun", from_lang="auto", target_lang="zh"):
    logging.info(f"translating using [{translator_name}] from [{from_lang}] to [{target_lang}]...")

    if translator_name == "deepl":
        from translatepy.translators.deepl import DeeplTranslate
        deep_translator = DeeplTranslate()
        ret = deep_translator.translate_html(html=input_html, source_language=from_lang,
                                             destination_language=target_lang)
        logging.info(ret)
        return ret
    elif translator_name == "aliyun":
        from lib.translators.aliyun import AliyunTranslator
        aliyun_translator = AliyunTranslator()

        ret = aliyun_translator.translate_html(input_html=input_html, source_language=from_lang,
                                               target_language=target_lang)
        logging.debug(ret)
        return ret

    else:
        logging.error("unimplemented yet.")
        return "unimplemented yet"
