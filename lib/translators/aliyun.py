# -*- coding: utf-8 -*-
import logging
import os
import sys

from alibabacloud_alimt20181012.client import Client as alimt20181012Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_20181012_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

Aliyun_Translator_Word_Limit = 5000
Aliyun_Translator_Error_Code_Doc = "https://help.aliyun.com/document_detail/158244.html"

Aliyun_Env_Id_Key = "ALIYUN_ACCESS_KEY_ID"
Aliyun_Env_Secret_Key = "ALIYUN_ACCESS_KEY_SECRET"


def default_result_html_when_error(translator: str) -> str:
    return f"<p><b>Translate failed.</b></p><p>translator <i>{translator}</i></p>"


class AliyunTranslator:
    client: alimt20181012Client
    translator_name: str = "aliyun"

    def __init__(self,
                 access_key_id: str = None,
                 access_key_secret: str = None,
                 ):
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        _id = access_key_id
        _secret = access_key_secret
        try:
            from dotenv import load_dotenv
            load_dotenv()
            # read credentials from env

            if not _id:
                _id = os.environ[Aliyun_Env_Id_Key]
            if not _secret:
                _secret = os.environ[Aliyun_Env_Secret_Key]
        except KeyError as e:
            logging.error(f"env key not found. {e.args}")
            sys.exit(-1)

        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=_secret
        )
        # 访问的域名
        config.endpoint = f'mt.aliyuncs.com'

        self.client = alimt20181012Client(config)

        logging.info("load translator aliyun done.")

    def translate_html(self,
                       input_html: str = '<html><p>hello world</p></html>',
                       source_language: str = 'auto',
                       target_language: str = 'zh',
                       ) -> str:
        translate_general_request = alimt_20181012_models.TranslateGeneralRequest(
            source_text=input_html,
            source_language=source_language,
            target_language=target_language,
            scene='general',
            format_type='html',
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            resp = self.client.translate_general_with_options(translate_general_request, runtime)
            resp_data = resp.body.data
            if resp.body.code == "200":
                result_html = resp_data.translated
                result_word_count = resp_data.word_count
                if int(result_word_count) > Aliyun_Translator_Word_Limit:
                    logging.warning("too many word for aliyun translator")
                return result_html
            else:
                logging.error(f"ERR: code {resp.body.code} msg {resp.body.message}")
                logging.error(f"reference translator's doc for help. link:{Aliyun_Translator_Error_Code_Doc}")
            logging.debug("resp data")
            logging.debug(resp_data)
        except Exception as error:
            err = UtilClient.assert_as_string(error.message)
            logging.warning(err)
        return default_result_html_when_error(self.translator_name)


# if __name__ == '__main__':
#     client = AliyunTranslator()
#     test_html = "<p>Hey Jude, don't be <b>afraid</b>Sing a sad song and you'll feel <p>better</p></p>"
#     ret = client.translate_html(test_html)
#     print(ret)
