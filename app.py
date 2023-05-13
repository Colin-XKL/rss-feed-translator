from __future__ import annotations

import logging
import xml.parsers.expat
from typing import Callable

import requests
import xmltodict
from flask import Flask, request, Response, render_template
from functools import lru_cache

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/translate_test')
def translate_test():
    logging.info("api hit")
    translated = translate_html("""<div><h1>Hello world!</h1><p>keep it up, you are awesome</p></div>""")
    return translated


@app.route('/translate', methods=['GET'])
def fetch_and_translate_feed():
    logging.info("fetch remote feed")
    feed_url = request.args.get('feed_url')
    translator = request.args.get('translator') or "aliyun"
    source_lang = request.args.get("source_lang") or "auto"
    target_lang = request.args.get("target_lang") or "zh"

    resp = requests.get(feed_url)
    # print(resp.content)
    xml_content = resp.content

    # pprint.pprint(d)
    ret = translate_feed(xml_content, translator=translator, source_lang=source_lang, target_lang=target_lang)

    return Response(xmltodict.unparse(ret), mimetype='text/xml')


@app.route('/feed_parse_test')
def feed_parse_test():
    logging.info("feed parse test hit.")
    # test_xml_fp = '/Users/colin/Downloads/tttt/rss20.xml'
    test_xml_fp = '/Users/colin/Downloads/tttt/feed.xml'
    with open(test_xml_fp, 'r') as f:
        xml_str = f.read()
        ret = translate_feed(xml_str, translator='aliyun', source_lang="auto", target_lang='zh')

    return ret


def check_is_array(item) -> bool:
    return hasattr(item, "__len__") and type(item) is not str and type(item) is not dict


def check_is_dict(item) -> bool:
    return type(item) is dict


def recursive_find_node_and_apply(target: dict, field: str, func: Callable):
    if check_is_dict(target):
        for k in target:
            if target.get(k, None) and k == field:
                if check_is_array(target[k]):
                    logging.warning("unexpected type, make sure the field always point to a leaf node.")
                elif check_is_dict(target[k]):
                    if target[k].get('#text', None):
                        # special handling for xml #text attr
                        target[k]['#text'] = func(target[k]['#text'])
                    else:
                        logging.warning("unexpected structure.")
                        logging.warning(target[k])
                else:
                    target[k] = func(target[k])
                continue

            target[k] = recursive_find_node_and_apply(target[k], field, func)

    elif check_is_array(target):
        for index, item in enumerate(target):
            target[index] = recursive_find_node_and_apply(item, field, func)
    else:  # is str or something like that
        # target = func(target)

        return target
    return target


def get_find_nodes_and_translate_func(translator: str, source_lang: str, target_lang: str):
    def check_and_manipulate(val):
        try:
            if check_is_dict(val) and val.get("#text", None):
                pass
            elif check_if_only_has_link(val):
                return val
            else:
                # return maniputate_func(val)
                return translate_html(val)
        except xml.parsers.expat.ExpatError:
            pass
        except TypeError:
            logging.warning("type error")
            # logging.warning(val)
            logging.warning(type(val))

        return translate_html(val, translator_name=translator, from_lang=source_lang, target_lang=target_lang)

    return check_and_manipulate


def translate_feed(xml_str: str | bytes, translator: str, source_lang: str, target_lang: str) -> dict:
    parsed = xmltodict.parse(xml_str)
    # pprint.pprint(parsed)
    if parsed.get('rss', None) or parsed.get('feed', None):  # rss or atom
        # if parsed.get('rss', None):  # rss
        # logging.info("rss feed")
        # pprint.pprint(parsed)

        field_to_translate = ["title", "content", "description", "summary"]
        ret = parsed
        for field in field_to_translate:
            ret = recursive_find_node_and_apply(ret, field, get_find_nodes_and_translate_func(source_lang=source_lang,
                                                                                              target_lang=target_lang,
                                                                                              translator=translator))

        #
        # from jsonpath_ng import jsonpath, parse
        #
        # # A robust parser, not just a regex. (Makes powerful extensions possible; see below)
        # jsonpath_expr = parse('foo[*].baz')
        #
        #

        # # parsed['rss']['channel']['title'] = "Hello Feed"
        # N = parsed['rss']['channel']['item']
        #
        # if hasattr(N, '__len__') and (not isinstance(N, str)):  # array
        #     for item in N:
        #         # pprint.pprint(item)
        #
        #         item['title'] = translate_html(item['title'])
        #         if item['content']:
        #             item['content'] = check_and_translate(item, 'content')
        #         if item['description']:
        #             item['description'] = check_and_translate(item, 'description')
        # else:  # single item
        #     item = parsed['rss']['channel']['item']
        #     item['title'] = translate_html(item['title'])
        #     if item['content']:
        #         item['content'] = check_and_translate(item, 'content')
        #     if item['description']:
        #         item['description'] = check_and_translate(item, 'description')
        #
        # ret = xmltodict.unparse(parsed)

    # elif parsed.get('feed', None):  # atom
    # logging.info("atom feed")
    # entry_list = parsed['feed']['entry']
    # if hasattr(entry_list, '__len__') and (not isinstance(entry_list, str)):  # array
    #     for item in entry_list:
    #         item['title'] = translate_html(item['title'])
    #         if item['content']:
    #             item['content'] = check_and_translate(item, 'content')
    #         item['description'] = check_and_translate(item, 'description')
    # else:
    #     item = parsed['feed']['entry']
    #     item['title'] = translate_html(item['title'])
    #     if item['content']:
    #         item['content'] = check_and_translate(item, 'content')
    #     if item['description']:
    #         item['description'] = check_and_translate(item, 'description')
    # ret = xmltodict.unparse(parsed)
    else:  # else
        ret = "Unimplemented yet"
    return ret
    # return


# def check_and_translate(item, key):
#     if key in item:
#         try:
#             if check_if_only_has_link(item[key]):
#                 # ignore for only link
#                 pass
#             else:
#                 return translate_html(item[key])
#         except xml.parsers.expat.ExpatError:
#             pass
#         except TypeError:
#
#             logging.warning("type error")
#             # logging.warning(item[key])
#             pprint.pprint(item)
#
#         return item[key]
#     else:
#         return None


def check_if_only_has_link(input_xml: str) -> bool:
    item = xmltodict.parse(input_xml)
    item.pop('a', None)
    return len(item) == 0


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


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
