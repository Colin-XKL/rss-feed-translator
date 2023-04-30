import logging
import pprint
import xml.parsers.expat

import xmltodict
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


@app.route('/feed_parse_test')
def feed_parse_test():
    logging.info("feed parse test hit.")
    test_xml_fp = '/Users/colin/Downloads/tttt/rss20.xml'
    with open(test_xml_fp, 'r') as f:
        xml_str = f.read()
        ret = translate_feed(xml_str)

    return ret


def translate_feed(xml_str: str) -> str:
    parsed = xmltodict.parse(xml_str)
    # pprint.pprint(parsed)
    if parsed.get('rss', None):  # rss
        parsed['rss']['channel']['title'] = "Hello Feed"
        N = parsed['rss']['channel']['item']

        if hasattr(N, '__len__') and (not isinstance(N, str)):
            for item in N:
                # pprint.pprint(item)

                item['title'] = translate_html(item['title'])
                try:
                    if check_if_only_has_link(item['description']):
                        # ignore for only link
                        continue
                    else:
                        item['description'] = translate_html(item['description'])
                except xml.parsers.expat.ExpatError:
                    pass

        ret = xmltodict.unparse(parsed)
    else:  # else atom feed etc.
        ret = "Unimplemented yet"
    return ret


def check_if_only_has_link(input_xml: str) -> bool:
    item = xmltodict.parse(input_xml)
    item.pop('a', None)
    return len(item) == 0


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
