#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time ： 2023/12/8 2:12
@Auth ： Xq
@File ：HenanSxzXpath.py.py
@IDE ：PyCharm
"""


henansxz_ele_dict = {
    "details-button": '#details-button',
    'proceed-link': '#proceed-link',
    'input_text': 'x://input[@type="text"]',
    'input_password': 'x://input[@type="password"]',
    'capture_img': 'x://*[@id="app"]/div/div/form/div[5]/div/div/div[2]/img',
    'capture_img_frame': 'x://*[@id="app"]/div/div/form/div[5]/div/div/div[1]/div/input',
    'login_button': 'x://*[@id="app"]/div/div/form/div[6]/div/button',
    'oms_button': 'x://*[@id="app"]/section/section/div/div/div/div/div[4]/div[2]/div/div/div/div/div/div[1]',
    'sxz_button': 'x://*[@id="app"]/section/section/div/div/div/div/div[4]/div[2]/div/div/div/div/div/div[4]/p',

    'ddglkh_button3': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[4]/li/div/span', # 调度考核管理 3
    'ddglkh_button3_8': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[4]/li/ul/div[8]/a/li/span', # 风光功率预测考核日考核数据汇总 3-8
    'ddglkh_button3_8_L111': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/span[2]',# 点击风电场
    'ddglkh_button3_8_L111_st': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[1]/div/div/input',
    'ddglkh_button3_8_L111_et': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[2]/div/div/input',
    'ddglkh_button3_8_L111_search': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[2]/div/button/span',
    'ddglkh_button3_8_L111_data': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[3]/div[2]/div/div[3]/table/tbody/tr',
    'ddglkh_button3_11': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[4]/li/ul/div[11]/a/li/span', # 有功功率变化日考核结果 3-11
    'ddglkh_button3_11_L111': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/span[2]',    # 点击风电场
    'ddglkh_button3_11_L111_st': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[1]/div[1]/div/div/div/input',
    'ddglkh_button3_11_L111_et': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[1]/div[2]/div/div/div/input',
    'ddglkh_button3_11_L111_data': 'x://*[@id="app"]/div/div[2]/section/div/div/form/div[2]/div[2]/div/div[2]/div/div[3]/table/tbody/tr',

    'jsglkh_button4': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/div/span', # 技术考核管理 4
    'jsglkh_button4_1': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[1]/a/li/span', # 动态无功装置补偿可用率 4-1
    'jsglkh_button4_1_L111': 'x://*[@id="pane-first"]/div/div/form/div[1]/div/div[1]/div[2]/div[1]/div[2]/div/div[1]/span[2]',
    'jsglkh_button4_1_L111_st': 'x://*[@id="pane-first"]/div/div/form/div[2]/div[1]/div/div/input',
    'jsglkh_button4_1_L111_et': 'x://*[@id="pane-first"]/div/div/form/div[2]/div[2]/div/div/input',
    'jsglkh_button4_1_L111_search': 'x://*[@id="pane-first"]/div/div/form/div[2]/div[2]/div/button/span',
    'jsglkh_button4_1_L111_data': 'x://*[@id="pane-first"]/div/div/form/div[2]/div[3]/div[2]/div/div[3]/table/tbody/tr',

    'jsglkh_button4_3': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[3]/li/div/span', #  有功调节能力考核 4-3
    'jsglkh_button4_3_1': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[3]/li/ul/div[1]/a/li/span', # acg 投运率
    'jsglkh_button4_3_1_L1': 'x://*[@id="app"]/div/div[2]/section/div/div/div[1]/div/div[2]/div/div[1]/div[1]/label/span/span', # 点击风场
    'jsglkh_button4_3_1_R2': 'x://*[@id="tab-1"]/span/i', # 日投运率
    'jsglkh_button4_3_1_R2_st': 'x://*[@id="pane-1"]/div[1]/div[1]/input',
    'jsglkh_button4_3_1_R2_et': 'x://*[@id="pane-1"]/div[1]/div[2]/input',
    'jsglkh_button4_3_1_R2_search': 'x://*[@id="pane-1"]/div[1]/button/span',
    'jsglkh_button4_3_1_R2_data': 'x://*[@id="pane-1"]/div[2]/div[3]/table/tbody/tr',

    'jsglkh_button4_4': 'x://*[@id="app"]/div/div[1]/div[2]/div[1]/div/ul/div[5]/li/ul/div[4]/a/li/span', # 并网电压曲线考核结果 4-4
    'jsglkh_button4_4_T3': 'x://*[@id="tab-2"]/span/i', # 日合格率结果
    'jsglkh_button4_4_T3_st': 'x://*[@id="pane-2"]/div[1]/div[1]/input',
    'jsglkh_button4_4_T3_et': 'x://*[@id="pane-2"]/div[1]/div[2]/input',
    'jsglkh_button4_4_T3_search': 'x://*[@id="pane-2"]/div[1]/button',
    'jsglkh_button4_4_T3_data': 'x://*[@id="pane-2"]/div[2]/div[3]/table/tbody/tr',
    'exit_username_button':'x://*[@id="dropdown-menu-3427"]/li[1]/span',
    'exit_username_button_exit':'x://*[@id="dropdown-menu-2414"]',

    'shoubaofuhe_button': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[2]/li/div',
    'shoubaofuhe_button_1': 'x://*[@id="app"]/section/section/aside/div/div/div[1]/div/ul/div[2]/li/ul/div[1]/a/li/span',
    'shangbao_date': 'x://*[@id="1$cell$2"]/div',
    'shangbao_state': 'x://*[@id="1$cell$3"]/div'


}
