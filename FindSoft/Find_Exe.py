#! /usr/bin/env python
# -*-coding:utf-8-*-
import os
import time
import pyautogui as pag
import pygetwindow as gw
from LogInfo.LogTools import Logger
from ProcessInfo.ProcessTools import ProcessCure


class FindExeTools(object):
    '''
    查询exe 工具
    '''

    def __init__(self):
        # self.log = Logger('../LogInfo/app.log') # 运行main时候用这个
        self.log = Logger()
        self.button_path = self.find_button_path()
        self.moren_path = F'{self.button_path}moren.png'
        self.lianjie_path = F'{self.button_path}lianjie.png'
        self.queren_path = F'{self.button_path}queren.png'
        self.yunxu_path = F'{self.button_path}yunxu.png'
        self.guanbi_path = F'{self.button_path}guanbi.png'
        self.yanzhengma_path = F'{self.button_path}yanzhengma.png'
        self.oms_path = F'{self.button_path}oms.png'

    def find_button_path(self):
        '''
        按钮绝对位置
        :return:  按钮绝对位置
        '''
        folder_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        button_path = F'{folder_path}{os.sep}Image{os.sep}icon{os.sep}button{os.sep}'
        return button_path

    def find_soft(self, process_name='iscpclient.exe'):
        '''
        查找软件
        :param process_name:  进程名称
        :return:

        '''
        PT = ProcessCure()
        time.sleep(5)
        PT.admin_kill_process(process_name)

        self.log.info(F'查找当前运行的{process_name},并结束进程')
        time.sleep(3)
        pag.FAILSAFE = False
        self.log.info(F'查找{process_name},并运行程序')
        # pag.press("win")
        # time.sleep(2)
        # pag.typewrite("sdk")
        # time.sleep(2)
        # pag.press("enter")
        # pag.press("enter")
        # time.sleep(2)
        import subprocess
        process_name =F'C:{os.sep}Program Files{os.sep}iscpclient{os.sep}bin{os.sep}iscpclient.exe'
        if not  os.path.isfile(process_name):
            process_name = F'..{os.sep}ExeSoft{os.sep}iscpclient{os.sep}bin{os.sep}iscpclient.exe'
        subprocess.Popen(process_name)
        time.sleep(3)
        res = gw.getWindowsWithTitle('安全接入网关SDK')[0]
        res.maximize()
        time.sleep(3)
        try:
            self.click_button(self.moren_path)
            self.log.info(F'点击SDK默认按钮')
        except Exception as e:
            print(e,111)
        time.sleep(3)
        try:
            self.click_button(self.lianjie_path)
            self.log.info(F'SDK连接中')
        except Exception as e:
            print(e,112)
        time.sleep(3)
        # self.click_button(self.queren_path)
        # pag.press("enter")
        self.log.info(F'SDK确认中')

        res = gw.getWindowsWithTitle('安全接入网关SDK')[0]
        self.log.warning(F'确定SDK已经安装到本机！')
        self.log.info(F'SDK最小化')

        res.minimize()

    def click_button(self, image_path):
        '''
        点击图片
        :param image_path:  图片地址
        :return: 位置信息
        '''
        location = pag.locateOnScreen(image=image_path, confidence=0.7)

        pag.doubleClick(location)
        time.sleep(1)
        # print(location)

        return location

# if __name__ == '__main__':

#     FEX = FindExeTools()
#     FEX.find_soft()
