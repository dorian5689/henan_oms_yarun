#! /usr/bin/env python
# -*-coding:utf-8-*-
import os
import json
import requests


# 钉钉开放API的相关信息


class DingApiTools(object):
    def __init__(self, appkey_value=None, appsecret_value=None, chatid_value=None):
        self.appkey = appkey_value
        self.appsecret = appsecret_value
        self.chatid = chatid_value

    def get_access_token(self):
        """
        获取 access_token
        :return:  access_token
        """

        url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (self.appkey, self.appsecret)

        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        data = {'appkey': self.appkey,
                'appsecret': self.appsecret}
        req = requests.request('GET', url, data=data, headers=headers)
        access_token = req.json()["access_token"]

        return access_token

    def get_media_id(self, image_path):
        """
         获得图片media_id
        :param image_path:  图片地址
        :return:  图片 media_id
        """
        access_token = self.get_access_token()

        url = 'https://oapi.dingtalk.com/media/upload?access_token=%s&type=file' % access_token
        files = {'media': open(image_path, 'rb')}
        data = {'access_token': access_token,
                'type': 'file'}
        response = requests.post(url, files=files, data=data)
        res_json = response.json()
        return res_json["media_id"]

    # 根据 media_id 去推送消息，还需要获取钉钉群的 chatid.
    def send_image(self, image_path):
        """
        发送图片
        :param image_path:
        :return:
        """
        access_token = self.get_access_token()
        media_id = self.get_media_id(image_path)

        url = 'https://oapi.dingtalk.com/chat/send?access_token=' + access_token
        header = {
            'Content-Type': 'application/json'
        }
        data = {'access_token': access_token,
                'chatid': self.chatid,
                'msgtype': 'image',
                'image': {'media_id': media_id}}
        r = requests.request('POST', url, data=json.dumps(data), headers=header)
        status_code = r.status_code
        if status_code == 200:
            return F'上传图片成功'
        else:
            raise F'上传图片失败'

    # chatid 获取的方式是可以在开发者后台去获取


if __name__ == "__main__":
    """
    参考:
    """

    appkey = 'dingf4i7j3gysejztafz'  # image测试
    appsecret = 'dKXLDK8yNzaKcXFi_fBHDNvN2B0eTt9dtm0YHOS1H7mYUHxcRASXgwb5oixmKs5y'  # image测试
    chatid = "chat984cfb46cbfa855ac55fd932467cacbd"  # image测试
    image_path = F"..{os.sep}Image{os.sep}Roads{os.sep}road.jpg"  # 这里直接定位到图片了
    DAT = DingApiTools(appkey, appsecret, chatid)
    res = DAT.send_image(image_path)
    print(res)