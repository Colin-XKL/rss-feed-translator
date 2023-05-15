from __future__ import annotations
import logging
import os

import requests
import xmltodict
from flask import Flask, request, Response, render_template

from lib.feed_transformers.utils import translate_feed
from lib.translators.common import translate_html

# load env
from dotenv import load_dotenv

load_dotenv()

isDebug = os.environ.get("FLASK_DEBUG") == "true"
logLevel = os.environ.get("LOGGING_LEVEL", "DEBUG")
port = os.environ.get("PORT", "6000")

# set logging
logging.basicConfig(level=logLevel, format='%(asctime)s %(levelname)s %(message)s')

# load sentry if necessary
if sentry_dsn := os.environ.get("SENTRY_DSN", None):
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[
            FlaskIntegration(),
        ],
        traces_sample_rate=1.0
    )
    logging.info("sentry loaded.")

# load main app
app = Flask(__name__)
logging.info("rss-feed-translator started.")


@app.route('/')
def home_page():
    return render_template('index.html')


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


@app.route('/translate_test')
def translate_test():
    logging.info("api hit")
    translated = translate_html("""<div><h1>Hello world!</h1><p>keep it up, you are awesome</p></div>""")
    return translated


if __name__ == '__main__':
    app.run(debug=True if isDebug else False, port=int(port) if port.isdigit() else 6000, host='0.0.0.0')
