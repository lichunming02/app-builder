# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""animal recognize component."""

import base64
import json

from appbuilder.core.component import Component
from appbuilder.core.components.animal_recognize.model import *
from appbuilder.core.message import Message
from appbuilder.core._client import HTTPClient
from appbuilder.core._exception import AppBuilderServerException


class AnimalRecognition(Component):
    r"""
       用于识别一张图片，即对于输入的一张图片（可正常解码，且长宽比较合适），输出动物识别结果。

       Examples:

       ... code-block:: python

           import appbuilder
           # 请前往千帆AppBuilder官网创建密钥，流程详见：https://cloud.baidu.com/doc/AppBuilder/s/Olq6grrt6#1%E3%80%81%E5%88%9B%E5%BB%BA%E5%AF%86%E9%92%A5
           os.environ["APPBUILDER_TOKEN"] = '...'

           animal_recognition = appbuilder.AnimalRecognition()
           with open("./animal_recognition_test.png", "rb") as f:
               out = self.component.run(appbuilder.Message(content={"raw_image": f.read()}))
           print(out.content)

        """
    @HTTPClient.check_param
    def run(self, message: Message, timeout: float = None, retry: int = 0) -> Message:
        r""" 动物识别

                    参数:
                       message (obj: `Message`): 输入图片或图片url下载地址用于执行识别操作. 举例: Message(content={"raw_image": b"..."})
                       或 Message(content={"url": "https://image/download/url"}).
                       timeout (float, 可选): HTTP超时时间
                       retry (int, 可选)： HTTP重试次数

                     返回: message (obj: `Message`): 识别结果. 举例: Message(name=msg, content={'result': [{'name':
                     '国宝大熊猫', 'score': '0.945917'}, {'name': '秦岭四宝', 'score': '0.0417291'}, {'name': '团团圆圆',
                     'score': '0.00584368'}, {'name': '圆仔', 'score': '0.000846628'}, {'name': '棕色大熊猫',
                     'score': '0.000538988'}, {'name': '金丝猴', 'score': '0.000279618'}]}, mtype=dict)
        """
        inp = AnimalRecognitionInMsg(**message.content)
        req = AnimalRecognitionRequest()
        if inp.raw_image:
            req.image = base64.b64encode(inp.raw_image)
        if inp.url:
            req.url = inp.url
        req.top_num = 6
        req.baike_num = 0
        result = self._recognize(req, timeout, retry)
        result_dict = proto.Message.to_dict(result)
        out = AnimalRecognitionOutMsg(**result_dict)
        return Message(content=out.dict())

    def _recognize(self, request: AnimalRecognitionRequest, timeout: float = None,
                   retry: int = 0) -> AnimalRecognitionResponse:
        r"""调用底层接口进行动物识别
                   参数:
                       request (obj: `AnimalRecognitionRequest`) : 动物识别输入参数
                   返回：
                       response (obj: `AnimalRecognitionResponse`): 动物识别返回结果
               """
        if not request.image and not request.url:
            raise ValueError("one of image or url must be set")

        data = AnimalRecognitionRequest.to_dict(request)
        if self.http_client.retry.total != retry:
            self.http_client.retry.total = retry
        headers = self.http_client.auth_header()
        headers['content-type'] = 'application/x-www-form-urlencoded'
        url = self.http_client.service_url("/v1/bce/aip/image-classify/v1/animal")
        response = self.http_client.session.post(url, headers=headers, data=data, timeout=timeout)
        self.http_client.check_response_header(response)
        data = response.json()
        self.http_client.check_response_json(data)
        request_id = self.http_client.response_request_id(response)
        self.__class__._check_service_error(request_id, data)
        animalRes = AnimalRecognitionResponse.from_json(json.dumps(data))
        animalRes.request_id = request_id
        return animalRes

    @staticmethod
    def _check_service_error(request_id: str, data: dict):
        r"""个性化服务response参数检查
            参数:
                request_id (str) : 请求ID
                data (dict) : 动物识别body返回
            返回：
                无
        """
        if "error_code" in data or "error_msg" in data:
            raise AppBuilderServerException(
                request_id=request_id,
                service_err_code=data.get("error_code"),
                service_err_message=data.get("error_msg")
            )
