from __future__ import annotations

import logging

import xmltodict
import xml.parsers.expat
from typing import Callable

from lib.translators.common import translate_html


def translate_feed(xml_str: str | bytes, translator: str, source_lang: str, target_lang: str) -> dict:
    parsed = xmltodict.parse(xml_str)
    # pprint.pprint(parsed)
    if parsed.get('rss', None) or parsed.get('feed', None):  # rss or atom

        field_to_translate = ["title", "content", "description", "summary"]
        ret = parsed
        for field in field_to_translate:
            ret = recursive_find_node_and_apply(ret, field, get_find_nodes_and_translate_func(source_lang=source_lang,
                                                                                              target_lang=target_lang,
                                                                                              translator=translator))
    else:  # else
        ret = "Unimplemented yet"
    return ret


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


def check_if_only_has_link(input_xml: str) -> bool:
    item = xmltodict.parse(input_xml)
    item.pop('a', None)
    return len(item) == 0


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
