#! /usr/bin/env python
# -*-coding:utf-8-*-

import time
import cv2
import numpy as np
import mss
import os
from pynput.mouse import Button

from FindSoft.Find_Exe import FindExeTools
from MacInfo.ChangeMAC import SetMac

import os

father_path = os.path.dirname(os.getcwd())


class Change_Uk_Info(object):
    def select_comports(self):
        import serial.tools.list_ports

        num_device = 0
        for i in serial.tools.list_ports.comports():
            i = str(i)
            if 'USB' in i:
                num_device = i[-2]
        if num_device == 0:
            return
        return num_device

    def find_icon_coordinates(self, image):
        # 加载要识别的图片
        icon = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

        # 创建 MSS (Media Source) 对象
        with mss.mss() as sct:
            # 获取屏幕分辨率
            monitor = sct.monitors[1]  # 通常使用 monitor 1，根据你的设置而定

            # 截取整个屏幕
            screenshot = sct.shot(output="screenshot.png")

        # 加载要搜索的图像
        screenshot = cv2.imread('screenshot.png', cv2.IMREAD_GRAYSCALE)

        # 使用模板匹配来查找图片位置
        result = cv2.matchTemplate(screenshot, icon, cv2.TM_CCOEFF_NORMED)

        # 设置阈值，找到匹配的位置
        threshold = 0.99
        locations = np.where(result >= threshold)

        # 提取匹配位置的坐标
        icon_height, icon_width = icon.shape
        coordinates = list(zip(*locations[::-1]))  # 反转坐标

        # 在原始截图上绘制矩形框显示匹配位置
        for (x, y) in coordinates:
            cv2.rectangle(screenshot, (x, y), (x + icon_width, y + icon_height), (0, 255, 0), 2)

        # 保存包含标记的结果图像
        cv2.imwrite('result.png', screenshot)
        if len(coordinates)>3:
            return coordinates[-1]
        else:
            return coordinates[0]


    def select_use_device(self, ):
        from pynput.mouse import Controller

        # 创建鼠标控制器
        mouse = Controller()

        # 打开按钮坐标
        # openbutton = F'../Image/uk_button/openbutton.png'

        openbutton = os.path.abspath(
            father_path + os.path.sep + F'{os.sep}Image{os.sep}uk_button{os.sep}openbutton.png')
        # 当前文件的前两级目录

        # 调用函数并获取匹配坐标
        open_button_coor = self.find_icon_coordinates(openbutton)
        open_button_x = open_button_coor[0]
        open_button_y = open_button_coor[1]

        # 可用设备坐标
        use_device_path = os.path.abspath(
            father_path + os.path.sep + F'{os.sep}Image{os.sep}uk_button{os.sep}use_device_name.png')

        # use_device_path = F'../Image/uk_button/use_device_name.png'

        # 调用函数并获取匹配坐标
        use_device_coor = self.find_icon_coordinates(use_device_path)
        # print(use_device_coor)
        use_device_coor_x = use_device_coor[0]
        use_device_coor_y = use_device_coor[1]

        # 下拉框的坐标
        drop_coor_x = use_device_coor_x + (open_button_x - use_device_coor_x) // 2
        drop_coor_y = open_button_y

        # 移动鼠标到下拉框上面
        mouse.position = (drop_coor_x, drop_coor_y)

        # time.sleep(0.5)
        # 执行第一次左键单击，弹出下拉框选项
        mouse.click(Button.left, 1)

        # use_comports_num_path = "images/use_comports_num_path.png"
        use_comports_num = self.select_comports()
        use_comports_num_path = os.path.abspath(
            father_path + os.path.sep + F'{os.sep}Image{os.sep}uk_button{os.sep}port{os.sep}port_{use_comports_num}.png')

        # use_comports_num_path = F'../Image/uk_button/port/port_{use_comports_num}.png'

        # 下拉框选项的坐标
        drop_coor_new_x = drop_coor_x
        drop_coor_new_y = drop_coor_y

        flag = 0
        # 移动鼠标到下拉框中相应的选项上面
        while True:
            # time.sleep(0.5)
            mouse.position = (drop_coor_x, drop_coor_y)
            mouse.click(Button.left, 1)
            # time.sleep(1)
            try:
                it_exist = self.find_icon_coordinates(use_comports_num_path)
            except:
                it_exist = ()

            if flag == 10:
                break

            if it_exist:
                mouse.position = (drop_coor_x, drop_coor_y)

                # time.sleep(1)
                mouse.click(Button.left, 1)
                # time.sleep(1)
                break

            else:
                drop_coor_new_y += 10
                flag += 1
                # print((drop_coor_x, drop_coor_new_y))
                mouse.position = (drop_coor_x, drop_coor_new_y)

                # time.sleep(2)
                mouse.click(Button.left, 1)
                # time.sleep(2)

        # 移动鼠标到打开按钮上面
        mouse.position = (open_button_x, open_button_y)
        # time.sleep(0.5)
        # 左键单击按钮
        mouse.click(Button.left, 2)
        # time.sleep(0.5)

        from pynput.keyboard import Key, Controller

        keyboard = Controller()
        # 模拟按下Enter键
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        self.all_button()
        # try:
        #     # 全部关闭按钮
        #     # off_all_button = F'../Image/uk_button/off_all.png'
        #     off_all_button = os.path.abspath(
        #         father_path + os.path.sep + F'{os.sep}Image{os.sep}uk_button{os.sep}off_all.png')
        #
        #     off_all_button_coor = self.find_icon_coordinates(off_all_button)
        #     off_all_button_x = off_all_button_coor[0]
        #     open_button_y = off_all_button_coor[1]
        #     # 移动鼠标到打开按钮上面
        #     mouse.position = (off_all_button_x, open_button_y)
        #     time.sleep(1)
        #     # 左键单击按钮
        #     mouse.click(Button.left, 2)
        #     time.sleep(1)
        #     keyboard.press(Key.enter)
        #
        #     keyboard.release(Key.enter)
        # except:
        #     pass

    def all_button(self):
        try:
            from pynput.mouse import Controller

            # 创建鼠标控制器
            mouse = Controller()
            # 全部关闭按钮
            # off_all_button = F'../Image/uk_button/off_all.png'
            off_all_button = os.path.abspath(
                father_path + os.path.sep + F'{os.sep}Image{os.sep}uk_button{os.sep}off_all.png')

            off_all_button_coor = self.find_icon_coordinates(off_all_button)
            off_all_button_x = off_all_button_coor[0]
            open_button_y = off_all_button_coor[1]
            # 移动鼠标到全部关闭按钮上面
            mouse.position = (off_all_button_x, open_button_y)
            # 左键单击按钮
            mouse.click(Button.left, 2)

        except:
            pass

    def radio_switch(self, num):

        try:
            radio_button = os.path.abspath(
                father_path + os.path.sep + F'{os.sep}Image{os.sep}uk_button{os.sep}usb{os.sep}{num}.png')

            # radio_button = F'../Image/uk_button/usb/{num}.png'
            # print(radio_button)
            # 调用函数并获取匹配坐标
            matching_coordinates = self.find_icon_coordinates(radio_button)
            ra_x = matching_coordinates[0]
            ra_y = matching_coordinates[1]

            from pynput.mouse import Controller
            mouse = Controller()

            # 移动鼠标到打开按钮上面
            mouse.position = (ra_x, ra_y)
            # time.sleep(1)
            # 左键单击按钮
            mouse.click(Button.left, 1)
            # time.sleep(0.5)

        except:
            return ()

        return matching_coordinates

    # def run(self):
    #
    #     exe_path = R"C:\Users\54982\Desktop\西普莱集线器资料\Release\HUB_Control通用版.exe"
    #     process_name = F"HUB_Control通用版.exe"
    #     from AutoLogin.ProcessInfo.ProcessTools import ProcessCure
    #
    #     PT = ProcessCure()
    #     PT.admin_kill_process(process_name)
    #
    #     import subprocess
    #     subprocess.Popen(exe_path)
    #     time.sleep(3)
    #
    #     self.select_use_device()
    #     for i in range(2, 6):
    #         time.sleep(3)
    #         self.radio_switch(f'{i}')
    #         slect_zhuangtai_sql = F"select  usb序号,UK密钥MAC地址,外网oms账号,外网oms密码  from data_oms_uk  where usb序号='{i}' "
    #         data_info = MysqlCurd().query_sql_return_header_and_data(slect_zhuangtai_sql).values.tolist()
    #         for data in data_info:
    #             num = data[0]
    #             mac_address = data[1]
    #             print(num, mac_address)
    #             set_mac = SetMac()  # 00FFAABBCCDD
    #             new_mac = mac_address
    #             set_mac.run(new_mac)
    #             time.sleep(4)
    #             FT = FindExeTools()
    #             FT.find_soft()
    #             time.sleep(6)
    #
    #             time.sleep(3)
    #             self.radio_switch(f'{i}_1')

# if __name__ == '__main__':
# #     # FT = FindExeTools()
# #     # FT.find_soft()
# #     # import pyautogui
# #     # pyautogui.hotkey('win', 'd')
#
#
#     #
#     time.sleep(3)
#     CU = Change_Uk_Info()
#     CU.run()
