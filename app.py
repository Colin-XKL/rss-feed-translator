import logging

from flask import Flask

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/translate_test')
def translate_test():
    logging.info("api hit")
    translated = translate_html("""<div><h1>Hello world!</h1><p>keep it up, you are awesome</p></div>""")
    return translated


def translate_html(input_html, translator_name="deepl", from_lang="auto", target_lang="Chinese"):
    logging.info(f"translating using [{translator_name}] from [{from_lang}] to [{target_lang}]...")

    if translator_name == "deepl":
        from translatepy.translators.deepl import DeeplTranslate
        deep_translator = DeeplTranslate()
        ret = deep_translator.translate_html(html=input_html, source_language=from_lang,
                                             destination_language=target_lang)
        logging.info(ret)
        return ret

    else:
        logging.error("unimplemented yet.")
        return "unimplemented yet"


if __name__ == '__main__':
    app.run(debug=True, port=5000)
