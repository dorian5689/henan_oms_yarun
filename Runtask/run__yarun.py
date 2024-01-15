#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/30 19:03
@Auth ： Xq
@File ：run_zz_jk.py
@IDE ：PyCharm
"""

import os
import time

import schedule
from DrissionPage import ChromiumPage
from DrissionPage._configs.chromium_options import ChromiumOptions

from DataBaseInfo.MysqlInfo.MysqlTools import MysqlCurd
from FindSoft.Find_Exe import FindExeTools
from MacInfo.ChangeMAC import SetMac
from XpathConfig.HenanXpath import henan_ele_dict
import ddddocr
import re

import datetime
from DrissionPage.common import Keys

from Config.ConfigUkUsb import henan_wfname_dict_num
from ProcessInfo.ProcessTools import ProcessCure
from UkChange.run_ukchange import Change_Uk_Info
from DingInfo.DingBotMix import DingApiTools


class ReadyLogin(object):

    def __init__(self):
        pass

    def select_uk(self):
        CU = Change_Uk_Info()

        list_port = CU.select_comports()
        if list_port is None:
            return None, None
        exe_path = F'..{os.sep}ExeSoft{os.sep}HUB_Control通用版{os.sep}HUB_Control通用版.exe'
        process_name = F"HUB_Control通用版.exe"

        PT = ProcessCure()
        PT.admin_kill_process(process_name)

        import subprocess
        subprocess.Popen(exe_path)
        time.sleep(6)
        CU.select_use_device()

        import pygetwindow as gw
        res = gw.getWindowsWithTitle('HUB_Control通用版 示例程序')[0]
        time.sleep(3)
        return res, CU

    # def select_usb_id(self):
    #     from Config.ConfigUkUsb import henan_wfname_dict_num
    #     usb_ids = []
    #     for k, v in henan_wfname_dict_num.items():
    #         usb_ids.append(k)
    #     return usb_ids

    def change_usbid(self):
        res, CU = self.select_uk()
        from Config.ConfigUkUsb import henan_wfname_dict_num
        for i, uuid in henan_wfname_dict_num.items():
            from datetime import datetime
            # 获取当前时间
            current_time = datetime.now()
            # 格式化当前时间
            start_run_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            if res:
                res.maximize()
                time.sleep(1)
                CU.all_button()
                time.sleep(2)
                CU.radio_switch(f'{i}')
                time.sleep(3)
                res.minimize()
            try:
                slect_zhuangtai_sql = F"select  usb序号,UK密钥MAC地址,场站,外网oms账号,外网oms密码  from data_oms_uk  where usb序号='{i}' "

                data_info = MysqlCurd().query_sql_return_header_and_data(slect_zhuangtai_sql).values.tolist()
            except:
                new_nanfang = F'../DataBaseInfo/MysqlInfo/new_nanfang.yml'
                slect_zhuangtai_sql = F"select  usb序号,UK密钥MAC地址,场站,外网oms账号,外网oms密码,wfname_id  from data_oms_uk  where usb序号='{i}' and uuid ='{uuid}'  "

                data_info = MysqlCurd(new_nanfang).query_sql_return_header_and_data(slect_zhuangtai_sql).values.tolist()

            for data in data_info:
                userid = int(data[0])

                mac_address = data[1]
                wfname = data[2]
                set_mac = SetMac()
                new_mac = mac_address
                set_mac.run(new_mac)
                time.sleep(6)
                try:
                    FT = FindExeTools()
                    FT.find_soft()
                except:
                    break
                time.sleep(3)
                username = data[3]
                password = data[4]
                wfname_id = data[5]
                try:
                    from datetime import datetime
                    # 获取当前时间
                    current_time = datetime.now()
                    # 格式化当前时间
                    start_run_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    RB = RunSxz(username, password, wfname, userid, wfname_id, start_run_time)
                    try:
                        run_num = RB.run_sxz(userid)
                        if run_num == 1:
                            continue
                    except Exception as e:
                        run_times = 0
                        for _ in range(3):
                            run_num = RB.run_sxz(userid)
                            if run_num < 1:
                                run_times += 1
                            if run_times > 3:
                                return
                        print(f'已经运行了一次{e}')
                except Exception as e:
                    print(F'主函数问题Q')
                    pass

        return 1


class RunSxz(object):
    def __init__(self, username=None, password=None, wfname=None, userid=None, wfname_id=None, start_run_time=None):
        """
        基于谷歌内核
        """
        self.username = username
        self.password = password
        self.wfname = wfname
        self.userid = userid
        self.wfname_id = wfname_id
        self.start_run_time = start_run_time
        # self.sxz_token = F'c8eb8d7b8fe2a3c07843233bf225082126db09ab59506bd5631abef4304da29e'
        # 天润
        self.jf_token = F'c8eb8d7b8fe2a3c07843233bf225082126db09ab59506bd5631abef4304da29e'
        # 奈卢斯
        self.nls_token = F'acabcf918755694f2365051202cf3921a690594c1278e4b7fe960186dce58977'

        self.page = self.check_chrome()
        self.login = F"https://172.21.5.193:19070/app-portal/index.html"
        self.today = datetime.datetime.now().strftime("%Y-%m-%d")
        # 获取前一天的日期
        self.today_1 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        # 天润
        self.appkey = "dingtc3bwfk9fnqr4g7s"  # image测试
        self.appsecret = "C33oOe03_K5pitN_S2dUppBwgit2VnPW0yWnWYBM3GzogGKhdy2yFUGREl9fLICU"  # image测试
        self.chatid = "chatf3b32d9471c57b4a5a0979efdb06d087"  # image测试
        # 奈卢斯
        self.nls_appkey = "dingjk2duanbfvbywqzx"  # image测试
        self.nls_appsecret = "ICYb4-cvsvIk5DwuZY9zehc5UbpldqIClzS6uuIYFrhjU9z11guV6lold1qNqc2k"  # image测试
        self.nls_chatid = "chatf8ef1e955cf2c4e83a7e776e0011366c"  # image测试

        self.message_dl = {
            "msgtype": "markdown",
            "markdown": {
                "title": "OMS推送",
                "text":
                    F'第{self.wfname_id}个场站:{self.wfname}--已上报--电量--现场程序'
            }
        }
        self.message_cn = {
            "msgtype": "markdown",
            "markdown": {
                "title": "OMS推送",
                "text":
                    F'第:{self.wfname_id}个场站:{self.wfname}--已上报--储能--现场程序'
            }
        }

    def check_chrome(self):
        """
        有谷歌走谷歌,没有走edge
        暂时不打包谷歌,300M
        :return:
        """
        user_name = os.getlogin()

        try:
            co = ChromiumOptions()
            co.set_argument("--start-maximized")
            page = ChromiumPage(co)
            return page
        except Exception as e:
            try:
                browser_path = F'C:{os.sep}Users{os.sep}{user_name}{os.sep}AppData{os.sep}Local{os.sep}Google{os.sep}Chrome{os.sep}Application{os.sep}chrome.exe'
                co = ChromiumOptions().set_paths(browser_path=browser_path)
                co.set_argument("--start-maximized")
                page = ChromiumPage(co)
                return page

            except Exception as e:
                browser_path = F'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
                co = ChromiumOptions().set_paths(browser_path=browser_path)
                co.set_argument("--start-maximized")
                page = ChromiumPage(co)
                # print(F"异常值:{e}")
                print(F"找不到本机谷歌浏览器,使用的是edge!")
                return page

    def chrome_login_page(self, userid):

        try:
            # self.page.ele(F'{henan_ele_dict.get("again_post")}')
            # self.page.clear_cache(cookies=False)
            time.sleep(2)
            self.page.refresh()
            self.page.get(self.login)
            self.page.refresh()

            self.page.wait
            try:
                self.page.ele(F'{henan_ele_dict.get("details-button")}').click()
                self.page.ele(F'{henan_ele_dict.get("proceed-link")}').click()
            except:
                pass
            if int(userid) == 1:
                self.exit_username_login()

            time.sleep(3)
            self.page(F'{henan_ele_dict.get("input_text")}').input(self.username)
            time.sleep(2)
            self.page(F'{henan_ele_dict.get("input_password")}').input(self.password)
            time.sleep(2)

            cap_text = self.send_code()

            return cap_text

        except Exception as e:
            try:
                print(F'验证码erroor{e}')
                cap_text = self.chrome_login_page()
                return cap_text
            except:
                if not cap_text:
                    return

    def send_code(self):
        cap = self.page.ele(F'{henan_ele_dict.get("capture_img")}')
        cap.click()

        import os
        path = os.path.abspath(__file__)
        par_path = os.path.dirname(os.path.dirname(path))
        path = F"{par_path}{os.sep}Image{os.sep}CaptureImg"
        img_name = "验证码.png"
        img_path = F"{path}{os.sep}{img_name}"
        try:
            import shutil
            shutil.rmtree(path)
        except:
            pass
        cap.get_screenshot(path=img_path, name=img_name, )
        ocr = ddddocr.DdddOcr()
        with open(img_path, 'rb') as f:
            img_bytes = f.read()
        cap_text = ocr.classification(img_bytes)
        print(f"验证码:{cap_text}")
        # 验证码长度不等于5或者包含中文字符或者不包含大写字母再次运行
        if len(cap_text) != 5 or bool(
                re.search(u'[\u4e00-\u9fa5]', cap_text)):
            print(F' 验证码:{cap_text}')
            for num in range(10):
                cap_text = self.send_code()
                time.sleep(2)
                if len(cap_text) == 5 and re.match('^[a-zA-Z0-9]+$', cap_text):
                    return cap_text
        return cap_text

    def run_sxz(self, userid):
        cap_text = self.chrome_login_page(userid)
        self.page.ele(F'{henan_ele_dict.get("capture_img_frame")}').input(cap_text)

        self.page.ele(F'{henan_ele_dict.get("login_button")}').click()
        time.sleep(3)
        self.page.wait

        if "欢迎登陆" in self.page.html:
            cap_text = self.send_code()
            self.page.ele(F'{henan_ele_dict.get("capture_img_frame")}').input(cap_text)
            self.page.ele(F'{henan_ele_dict.get("login_button")}').click()  # 登录按钮
        if "验证码" in self.page.html:
            cap_text = self.send_code()
            self.page.ele(F'{henan_ele_dict.get("capture_img_frame")}').input(cap_text)
            self.page.ele(F'{henan_ele_dict.get("login_button")}').click()  # 登录按钮
        if "解析密码错误" in self.page.html:
            cap_text = self.send_code()
            self.page.ele(F'{henan_ele_dict.get("capture_img_frame")}').input(cap_text)
            self.page.ele(F'{henan_ele_dict.get("login_button")}').click()  # 登录按钮
        henan_oms_data = self.henan_data()

        self.page.ele(F'{henan_ele_dict.get("oms_button")}').click()
        time.sleep(6)
        self.page.wait
        # sxz
        table0 = self.page.get_tab(0)
        try:
            self.report_load_dl(table0, henan_oms_data)
        except:
            pass
        try:
            if userid in [6, 8, 10, 11]:
                self.report_load_cn(table0, henan_oms_data)
        except:
            pass
        try:
            self.exit_username_oms(table0)
            table0.close()
            try:
                self.page.quit()
                print("网页退出！")
            except:
                pass
            return 1


        except Exception as e:
            print(f'运行失败！')
            return 0

    def exit_username_login(self):
        try:
            res = self.page.ele('x://*[@id="app"]/section/header/div/div[2]/div/div/span').click()
        except:
            res = 0

        if res:
            self.page.ele('x:/html/body/ul/li[1]/span').click()
            self.page.ele('x:/html/body/div[2]/div/div[3]/button[2]').click()

        else:
            return

    def exit_username_oms(self, table0):
        table0.ele('x://*[@id="app"]/section/header/div/div[2]/div[1]/div/span').click()
        table0.ele('x://html/body/ul/li[1]/span').click()

        table0.ele('x://*[@id="app"]/section/header/div/div[2]/div[1]/div/span').click()
        table0.ele('x://html/body/ul/li[4]/span').click()
        try:
            table0.ele('x://html/body/div[23]/div/div[3]/button[2]/span').click()
        except:
            table0.ele('x://html/body/div[28]/div/div[3]/button[2]/span').click()

        time.sleep(2)

    def report_load_dl(self, table0, henan_oms_data):
        table0.ele(F'{henan_ele_dict.get("report_load")}').click()
        print(F'点击了收报负荷！')
        table0.ele(F'{henan_ele_dict.get("report_load_button_dl")}').click()
        self.page.wait

        if self.today_1 == table0.ele(F'{henan_ele_dict.get("upload_date")}').text:
            self.send_ding_dl(table0)
        else:
            table0.ele(F'{henan_ele_dict.get("send_battery")}').input(F'{henan_oms_data[0]}\ue007')
            table0.ele(F'{henan_ele_dict.get("upload_battery")}').input(F'{henan_oms_data[1]}\ue007')
            table0.ele(F'{henan_ele_dict.get("abandoned_battery")}').input(F'{henan_oms_data[2]}\ue007')
            self.upload_button_dl(table0)

    def send_ding_dl(self, table0):
        time.sleep(3)
        save_wind_wfname = self.save_pic(table0)
        from DingInfo.DingBotMix import DingApiTools
        # 天润
        DAT = DingApiTools(appkey_value=self.appkey, appsecret_value=self.appsecret, chatid_value=self.chatid)
        DAT.push_message(self.jf_token, self.message_dl)
        DAT.send_file(F'{save_wind_wfname}', 0)

        # 奈卢斯
        DATNLS = DingApiTools(appkey_value=self.nls_appkey, appsecret_value=self.nls_appsecret,
                              chatid_value=self.nls_chatid)
        DATNLS.push_message(self.nls_token, self.message_dl)
        DATNLS.send_file(F'{save_wind_wfname}', 0)

        self.update_mysql()

    def send_ding_cn(self, table0):
        time.sleep(3)
        save_wind_wfname = self.save_pic(table0)
        from DingInfo.DingBotMix import DingApiTools
        # 天润
        DAT = DingApiTools(appkey_value=self.appkey, appsecret_value=self.appsecret, chatid_value=self.chatid)
        DAT.push_message(self.jf_token, self.message_cn)
        DAT.send_file(F'{save_wind_wfname}', 0)

        # 奈卢斯
        DATNLS = DingApiTools(appkey_value=self.nls_appkey, appsecret_value=self.nls_appsecret,
                              chatid_value=self.nls_chatid)
        DATNLS.push_message(self.nls_token, self.message_dl)
        DATNLS.send_file(F'{save_wind_wfname}', 0)

        self.update_mysql()

    def save_pic(self, table0):
        import os
        import shutil
        from pathlib import Path

        img_path = Path(f"..{os.sep}Image{os.sep}save_wind{os.sep}{self.today_1}{os.sep}")
        directory = img_path.parent

        if directory.exists():
            # 如果目录存在且不为空，则递归删除整个目录及其内容
            shutil.rmtree(directory)
            # 然后重新创建该目录
            directory.mkdir(parents=True, exist_ok=True)

        # 对整页截图并保存
        save_wind_wfname = F"{img_path}{os.sep}{self.wfname}_程序.png"

        table0.get_screenshot(path=save_wind_wfname, full_page=True)

        # from PIL import ImageGrab
        # im = ImageGrab.grab()
        # save_wind_wfname = F"{img_path}{os.sep}{self.wfname}_程序.png"
        # im.save(save_wind_wfname)
        return save_wind_wfname

    def report_load_cn(self, table0, henan_oms_data):
        time.sleep(2)

        table0.ele(F'{henan_ele_dict.get("report_load")}').click()
        table0.ele(F'{henan_ele_dict.get("report_load_button_cn")}').click()
        if self.today_1 == table0.ele(F'{henan_ele_dict.get("upload_date")}').text:
            time.sleep(5)
            self.send_ding_cn()
        else:
            table0.ele(F'{henan_ele_dict.get("store_energy_max_charge_power_day")}').input(
                F'{float(henan_oms_data[3])}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_max_charge_power")}').input(F'{henan_oms_data[4]}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_max_discharge_power")}').input(F'{henan_oms_data[5]}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_day_charge_power")}').input(F'{henan_oms_data[6]}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_day_discharge_power")}').input(
                F'{int(henan_oms_data[7])}\ue007')
            table0.ele(F'{henan_ele_dict.get("store_energy_day_charge_power_times")}').input(
                F'{int(henan_oms_data[8])}\ue007')
            self.upload_button_cn(table0)

    def upload_button(self, table0):
        try:
            table0.ele(F'{henan_ele_dict.get("upload_battery_button")}').click()
            hadle_alert_true = table0.handle_alert(accept=True)
            print(F'这里是点击确定后的返回值！--{hadle_alert_true}')
        except Exception as e:
            table0.ele(F'{henan_ele_dict.get("upload_battery_button")}').click()
            hadle_alert_true = table0.handle_alert(accept=True)
            print(F'这里是点击确定后的返回值！--{hadle_alert_true}')
            pass

    def upload_button_dl(self, table0):
        self.upload_button(table0)
        self.send_ding_dl(table0)

    def upload_button_cn(self, table0):
        self.upload_button(table0)
        time.sleep(5)
        self.send_ding_cn(table0)

    def update_mysql(self):

        from DataBaseInfo.MysqlInfo.MysqlTools import MysqlCurd
        MC = MysqlCurd()
        from datetime import datetime
        # 获取当前时间
        current_time = datetime.now()
        # 格式化当前时间
        end_run_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        update_sql_success = F"update   data_oms  set  是否已完成 =1 ,填报开始时间 = '{self.start_run_time}',填报结束时间 = '{end_run_time}' where   日期='{self.today_1}' and 电场名称='{self.wfname}'"

        MC.update(update_sql_success)
        new_nanfang = F'../DataBaseInfo/MysqlInfo/new_nanfang.yml'
        NEWMC = MysqlCurd(new_nanfang)
        print(NEWMC.query_sql())
        NEWMC.update(update_sql_success)

    def henan_data(self):
        from DataBaseInfo.MysqlInfo.MysqlTools import MysqlCurd
        from ReadExcle.HenanOmsConfig import henan_oms_config, henan_oms_config_new

        try:
            MC = MysqlCurd()
            df_oms = MC.query_sql_return_header_and_data(henan_oms_config)
        except:
            new_nanfang = F'../DataBaseInfo/MysqlInfo/new_nanfang.yml'
            MC = MysqlCurd(new_nanfang)
            df_oms = MC.query_sql_return_header_and_data(henan_oms_config_new)

        time.sleep(1)
        henan_oms_data1 = df_oms.loc[
            (df_oms['电场名称'] == self.wfname) & (df_oms['日期'] == self.today_1), ['发电量', '上网电量', '弃电量',
                                                                                     '储能最大充电电力',
                                                                                     '储能最大放电电力', '储能日充电',
                                                                                     '储能日放电', '充电次数',
                                                                                     '放电次数']]

        import numpy as np
        henan_oms_data = np.nan_to_num(henan_oms_data1.values.tolist()[0])
        return henan_oms_data


def run_zz_jk_time():
    close_chrome()
    ReadyLogin().change_usbid()


def close_chrome():
    page = RunSxz().page
    page.get('https://www.baidu.com')

    try:
        page.quit()
    except:
        pass


if __name__ == '__main__':
    # run_zz_jk_time()

    print(F"自动化程序填报运行中,请勿关闭!")
    # print(F"保佑,保佑,正常运行!")
    schedule.every().day.at("00:20").do(run_zz_jk_time)
    schedule.every().day.at("00:40").do(run_zz_jk_time)
    while True:
        schedule.run_pending()

        time.sleep(1)
