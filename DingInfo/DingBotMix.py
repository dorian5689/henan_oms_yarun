#! /usr/bin/env python
# -*-coding:utf-8-*-
import os
import json
import requests
from LogInfo.LogTools import Logger

logger = Logger()


# 钉钉开放API的相关信息


class DingApiTools(object):
    """
    钉钉开放API的相关信息
    目前支持图片/文件上传/markdown
    后续支持卡片方式等
    """

    def __init__(self, appkey_value=None, appsecret_value=None, chatid_value=None):
        """
        初始化空值,在发送文字时候可不传
        :param appkey_value:
        :param appsecret_value:
        :param chatid_value:
        """
        self.appkey = appkey_value
        self.appsecret = appsecret_value
        self.chatid = chatid_value

    def get_access_token(self):
        """
        获取 access_token
        给图片/文件提供的
        :return:  access_token
        """

        url = "https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s" % (self.appkey, self.appsecret)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"appkey": self.appkey,
                "appsecret": self.appsecret}
        req = requests.request("GET", url, data=data, headers=headers)
        access_token = req.json()["access_token"]

        return access_token

    def get_media_id(self, file_path):
        """
         文件media_id
        :param file_path:  文件地址
        :return:  文件地址file_path
        """
        access_token = self.get_access_token()

        url = "https://oapi.dingtalk.com/media/upload?access_token=%s&type=file" % access_token
        files = {"media": open(file_path, "rb")}
        data = {"access_token": access_token,
                "type": "file"}
        response = requests.post(url, files=files, data=data)
        res_json = response.json()
        return res_json["media_id"]

    # 根据 media_id 去推送消息，还需要获取钉钉群的 chatid.
    def send_file(self, file_path, num):
        """
        发送图片
        :param file_path:
        :param type: 0 image  1 file
        :return:
        """
        access_token = self.get_access_token()
        media_id = self.get_media_id(file_path)

        url = "https://oapi.dingtalk.com/chat/send?access_token=" + access_token
        header = {
            "Content-Type": "application/json"
        }
        file_type = "image" if num == 0 else ("file" if num == 1 else num)
        message = {"access_token": access_token,
                   "chatid": self.chatid,
                   "msgtype": file_type
            ,
                   file_type: {"media_id": media_id}}

        response = requests.request("POST", url, data=json.dumps(message), headers=header)
        status_code = response.status_code

        if num == 0:
            if status_code == 200:
                logger.info(F"上传图片成功！")
                return F"上传图片成功！"
            else:
                logger.info(F"上传图片失败！")
                raise F"上传图片失败！"

        if num == 1:
            if status_code == 200:
                logger.info(F"上传文件成功！")
                return F"上传文件成功！"
            else:
                logger.info(F"上传文件失败")
                raise F"上传文件失败！"

    # chatid 获取的方式是可以在开发者后台去获取

    def push_message(self, access_token=None, message=None):
        """
        推送文本数据
        :param key_word:  设置的关键字
        :param web_hook:  机器人的webhook
        :param markdown:
        :return:
        """

        header = {
            "Content-Type": "application/json;charset=UTF-8"
        }

        web_hook = F"https://oapi.dingtalk.com/robot/send?access_token={access_token}"
        send_data = json.dumps(message)  # 将字典类型数据转化为json格式
        response = requests.post(url=web_hook, data=send_data, headers=header)
        status_code = response.status_code
        msg_type = message.get("msgtype")
        if msg_type == "markdown":
            if status_code == 200:

                logger.info(F"markdown 信息已经推送！")
                return F"markdown 信息已经推送！"
            else:
                logger.warning(F"markdown 信息推动失败！")
                raise F"markdown 信息推动失败"

        if msg_type == "text":
            if status_code == 200:
                logger.info(F"text 信息已经推送！")
                return F"text 信息已经推送！"
            else:
                logger.warning(F"text 信息推动失败！")
                raise F"text 信息推动失败！"


def run_upload_file_xqkj():
    """
    注意,需要写成你自己的相关值
    使用量参考: https://open-dev.dingtalk.com/?spm=dd_developers.homepage.0.0.21c24a97tNKLmE#/
    开发资源消耗
        应用开发与连接流资源
            付费 API 调用量
                119/10000
            API 请求并发量
                2/20
            连接流节点执行量
                0/1000
            Webhook 和 Stream 用量
                7/5000
    :return:
    """

    appkey = "dingf4i7j3gysejztafz"  # image测试
    appsecret = "dKXLDK8yNzaKcXFi_fBHDNvN2B0eTt9dtm0YHOS1H7mYUHxcRASXgwb5oixmKs5y"  # image测试
    chatid = "chat984cfb46cbfa855ac55fd932467cacbd"  # image测试
    file_path = F"..{os.sep}Image{os.sep}Roads{os.sep}road.jpg"  # 这里直接定位到图片了
    DAT = DingApiTools(appkey, appsecret, chatid)
    res = DAT.send_file(file_path, 0)
    file_path = F"..{os.sep}图片上传关键参数说明.docx"  # 这里直接定位到文件了了
    res = DAT.send_file(file_path, 1)


# 天润新能
def run_upload_file_trxn(file_path,num):
    """
    注意,需要写成你自己的相关值
    使用量参考: https://open-dev.dingtalk.com/?spm=dd_developers.homepage.0.0.21c24a97tNKLmE#/
    开发资源消耗
        应用开发与连接流资源
            付费 API 调用量
                119/10000
            API 请求并发量
                2/20
            连接流节点执行量
                0/1000
            Webhook 和 Stream 用量
                7/5000
    :return:
    """

    appkey = "dingtc3bwfk9fnqr4g7s"  # image测试
    appsecret = "C33oOe03_K5pitN_S2dUppBwgit2VnPW0yWnWYBM3GzogGKhdy2yFUGREl9fLICU"  # image测试
    chatid = "chatf3b32d9471c57b4a5a0979efdb06d087"  # image测试
    DAT = DingApiTools(appkey, appsecret, chatid)
    res = DAT.send_file(file_path,num)
    # file_path = F"..{os.sep}图片上传关键参数说明.docx"  # 这里直接定位到文件了了
    # res = DAT.send_file(file_path, 1)

def run_push_message_xqkj():
    """
    注意,需要写成你自己的相关值
    access_token  来源机器人,电脑查看
    markdown 支持在线图片链接，但是不支持本地图片(目前)
    text 正常文本数据

    :return:
    """
    title = "定时推送"
    access_token = "4ee44a8a4bf2fb8912dadc04396c3a17d7a819f1f99fc6a31f9a4a3bff5bc95e"
    #  markdoen 格式,函数会解析
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": "#### 文心一言图标 \n ![screenshot](https://ebui-cdn.bj.bcebos.com/yiyan-logo.png)\n ###### 00点05分发布 [百度一下](https://www.baidu.com) \n"
        }
    }

    # text 格式
    """    
    content = F"定时推送,数据已经上报！"
    message = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    """

    DAT = DingApiTools()
    DAT.push_message(access_token, message)


# if __name__ == "__main__":
#     """
#     参考: 图片上传关键参数说明.docx
#     """
#     # run_upload_file_xqkj()  # 图片/文件
#     # run_push_message_xqkj() # 文本/markdown
#     file_path = F"..{os.sep}Image{os.sep}roads{os.sep}road.jpg"  # 这里直接定位到图片了
#     run_upload_file_trxn(file_path,0)