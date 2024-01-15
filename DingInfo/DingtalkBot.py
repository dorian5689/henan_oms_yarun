#! /usr/bin/env python
# -*-coding:utf-8-*-
import json
import requests
from AutoLogin.LogInfo.LogTools import Logger


# 钉钉开放API的相关信息
class DingapiTools(object):
    """
    钉钉开放API的工具类
    """

    def __init__(self):
        self.log = Logger()

    def SendMessageDing(self, token, markdown):
        """
        发送信息到钉钉
        :param token: 相关组织获得的值
        :param markdown:发送的markdown信息
        :return:
        """
        webhook = f"https://oapi.dingtalk.com/robot/send?access_token={token}"
        header = {
            "Content-Type": "application/json",
            "Charset": "UTF-8"
        }
        message = {
            "msgtype": "markdown",
            "markdown": markdown
        }
        message_json = json.dumps(message)
        info = requests.post(url=webhook, data=message_json, headers=header)
        self.log.info(F'钉钉发送的数据为:{info.text}')
        return "发送成功"

    def push_message(self, web_hook, mess):
        # 另外一版
        key_word = "推送"

        header = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        message_body = {
            "msgtype": "markdown",
            "markdown": {
                "title": key_word,
                "text": mess

            },
            "at": {
                "atMobiles": [],
                "isAtAll": False
            }
        }
        send_data = json.dumps(message_body)  # 将字典类型数据转化为json格式
        ChatBot = requests.post(url=web_hook, data=send_data, headers=header)
        opener = ChatBot.json()
        if opener["errmsg"] == "ok":
            self.log.info(F'通知消息发送成功:{opener}')

            # print(u"%s 通知消息发送成功！" % opener)
        else:
            self.log.info(F'通知消息发送失败，原因:{opener}')

            # print(u"通知消息发送失败，原因：{}".format(opener))

    def getAccess_token(self):
        '''
        获取 access_token
        :return:  access_token
        '''
        _appkey = '你自己的appkey'
        _appkey = 'dingsdupi7pvqkijzvmb'
        _appkey = 'dingtc3bwfk9fnqr4g7s'  # 金风
        _appsecret = '你自己的appsecret'
        _appsecret = 'IDCIAGEaoxe17FjgxBwVsK3DJ2_AbKGJZQax7ds9XilJKp2hd_HIuVAzGXRfEhfP'
        _appsecret = 'C33oOe03_K5pitN_S2dUppBwgit2VnPW0yWnWYBM3GzogGKhdy2yFUGREl9fLICU'  # 金风

        url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (_appkey, _appsecret)

        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        data = {'appkey': _appkey,
                'appsecret': _appsecret}
        r = requests.request('GET', url, data=data, headers=headers)
        access_token = r.json()["access_token"]

        self.log.info(F'返回access_token:{access_token}')

        return access_token

    def getMedia_id(self, file_path):
        '''
         获得文件信息 id
        :param file_path:  文件路径
        :return:  文件id
        '''
        access_token = self.getAccess_token()

        url = 'https://oapi.dingtalk.com/media/upload?access_token=%s&type=file' % access_token
        files = {'media': open(file_path, 'rb')}
        data = {'access_token': access_token,
                'type': 'file'}
        response = requests.post(url, files=files, data=data)
        json = response.json()
        self.log.info(F'获取文件的media_id信息:{json}')
        return json["media_id"]

    # 根据 media_id 去推送消息，还需要获取钉钉群的 chatid.
    def SendFile(self, file_path):
        '''
        发送图片
        :param file_path:
        :return:
        '''
        access_token = self.getAccess_token()
        media_id = self.getMedia_id(file_path)
        # chatid = "chat19f245b8e1b2dea8340147330f7fa5a5"
        chatid = "chatf3b32d9471c57b4a5a0979efdb06d087"  # 金风
        url = 'https://oapi.dingtalk.com/chat/send?access_token=' + access_token
        header = {
            'Content-Type': 'application/json'
        }
        data = {'access_token': access_token,
                'chatid': chatid,
                'msgtype': 'image',
                'image': {'media_id': media_id}}
        r = requests.request('POST', url, data=json.dumps(data), headers=header)
        self.log.info(F'消息发送返回的状态:{r.json()}')
        self.log.warning(F'发送失败原因之一:没有权限,请开权限 qyapi_chat_manage')

        # todo  没有权限,请开权限 qyapi_chat_manage

    # chatid 获取的方式是可以在开发者后台去获取
    # 还有一种方式是 直接用代码创建一个会话群，可以返回一个 chatid
    def get_chatid(self):
        '''
        获取chatid
        :return:
        '''
        access_token = ''
        url = 'https://oapi.dingtalk.com/chat/create?access_token=%s' % access_token

        data = {'name': '群名称',
                'owner': '群主userid',
                'useridlist': ['成员列表userid']}  # 注意这边必须要加入群主的userid
        r = requests.post(url, data=json.dumps(data))
        mess = r.json()
        self.log.info(F'chatid的信息:{mess}')
class DingCard(object):
    '''
    钉钉推送卡片信息
    '''

    def __init__(self):
        pass


# if __name__ == "__main__":
#     DT = DingapiTools()
#     file_path = R'../DataInfo/河南/河南oms.xls'
#     DT.SendFile(file_path)
    # token 相关组织获得的值
    # token = "4ee44a8a4bf2fb8912dadc04396c3a17d7a819f1f99fc6a31f9a4a3bff5bc95e"
    # markdown = {""
    #             "title": "北京天气定时推送",
    #             "text": "#### 北京天气 @150XXXXXXXX \n 9度，西北风1级，空气良89，相对温度73% \n ![screenshot](http://www.tian-run.com/images/service1.jpg)\n ###### 10点20分发布 [天气](https://www.dingalk.com) \n"
    #             }
    # # 参考: https://open.dingtalk.com/document/orgapp/upload-media-files
    # DT = DingapiTools()
    # DT.SendMessageDing(token, markdown)
