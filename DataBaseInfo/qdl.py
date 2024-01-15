# %%
from sys import path

path.append('/home/user/wls_usr/nanfangzhongxingapp/wind_project')
from DataBaseInfo.PgCurd import my_database as md
from DataBaseInfo.HbaseCurd import Get_info_Hbase_south as GiHs
import pandas as pd
import datetime
import numpy as np
import sqlite3


def qdl_df():
    # %%
    sql = '''select
        w2.wfname ,
        w.wtid,
        w.wtname,
        w.protocolid
    from
        config.wtinfo w
    left join config.wfinfo w2 on
        w.wfid = w2.wfid
    where
        w2.wfname in ('润清','雅润','延津泽润','润金','泉山','飞翔','南阳凯润','金燕','泽润','驭风(卫南坡)','汤阴伏绿','嘉润')
        and w.wtname in ('EMSD', '能量管理','EMSD(二期)')
        '''
    data = md.real_pg(sql)

    # %%
    feature_agc = [
        'EMSD.PwrAt.Ra.F32.Benchmarking',  ##全场理论有功功率(标杆机组算法)
        'EMSD.PwrAt.Ra.F32.PlannedValue',  ##全场计划设定值
        'EMSD.PwrAt.Ra.F32.Theory'  ##全场理论功率（风速法）
    ]

    feature_emsd = [
        'EMSD.PwrAt.Ra.F32.PlannedValue',  ##AGC全场有功设定值的返回值
        'EMSD.PwrAt.Ra.F32.PlanValTimegird',  ##电网有功
        'EMSD.PwrAt.Ra.F32.Theory',  ##理论有功
        'EMSD.PwrAt.Ra.F32.Benchmarking',  ##标杆机组
        'EMSD.PwrAt.Ra.F32.Count'
    ]

    agc_wt = 410901711  ###EMSD
    emsd_wt = 411335701  ##EMSD
    sample_time = 30  # 采样频率30s
    day_num = 1
    GH = GiHs()

    def get_ration_ele(wfname, emsd_wt, day_num, sample_time):
        GH = GiHs()
        wfinfo = wfname
        start_time = (datetime.datetime.now() - datetime.timedelta(days=day_num)).strftime("%Y-%m-%d ") + '00:00:00.000'
        end_time = (datetime.datetime.now() - datetime.timedelta(days=day_num)).strftime("%Y-%m-%d ") + '23:59:59.000'
        # start_time = (datetime.datetime.now()).strftime("%Y-%m-%d ") + '00:00:00.000'
        # end_time = (datetime.datetime.now()).strftime("%Y-%m-%d ") + '23:59:59.000'

        # get_data_agc=GH.get_wtid_data(str(int(agc_wt)),start_time=start_time,end_time=end_time,sample=sample_time,info=feature_agc)
        get_data_EMSD = GH.get_wtid_data(str(int(emsd_wt)), start_time=start_time, end_time=end_time,
                                         sample=sample_time,
                                         info=feature_emsd)
        get_data_EMSD_limit = get_data_EMSD
        Benchmarking_str = 'EMSD.PwrAt.Ra.F32.Benchmarking'
        Theory_str = 'EMSD.PwrAt.Ra.F32.Theory'
        Plane_str = 'EMSD.PwrAt.Ra.F32.PlannedValue'
        if len(get_data_EMSD_limit[get_data_EMSD_limit['EMSD.PwrAt.Ra.F32.PlannedValue'] == 'NULL']) > 0:
            wfname = wfname + '集控存在' + str(
                len(get_data_EMSD_limit[get_data_EMSD_limit['EMSD.PwrAt.Ra.F32.PlannedValue'] == 'NULL']) / 2) + \
                     '分钟空值，请现场人工核对限电量！'

            get_data_EMSD_limit = get_data_EMSD_limit[get_data_EMSD_limit['EMSD.PwrAt.Ra.F32.PlannedValue'] != 'NULL']
        # if wfname=='金燕':
        #    get_data_EMSD_limit[Benchmarking_str]=get_data_EMSD_limit[Benchmarking_str]/1000
        if int(emsd_wt) == 410727701:
            wfname = '科兴二期'

        if wfname == '飞翔':
            def get_right(a):
                if a > 70000:
                    a = 70000
                return a

            get_data_EMSD_limit['EMSD.PwrAt.Ra.F32.Benchmarking'] = get_data_EMSD_limit[
                'EMSD.PwrAt.Ra.F32.Benchmarking'].apply(lambda x: get_right(x))

            get_data_EMSD_limit['EMSD.PwrAt.Ra.F32.Theory'] = get_data_EMSD_limit['EMSD.PwrAt.Ra.F32.Theory'].apply(
                lambda x: get_right(x))

        Benchmarking_limit = get_data_EMSD_limit[get_data_EMSD_limit[Plane_str] < get_data_EMSD_limit[Benchmarking_str]]
        Benchmarking_limit_value = (Benchmarking_limit[Benchmarking_str] - Benchmarking_limit[
            Plane_str]).sum() * sample_time / 3600
        Theory_limit = get_data_EMSD_limit[get_data_EMSD_limit[Plane_str] < get_data_EMSD_limit[Theory_str]]
        Theory_limit_value = (Theory_limit[Theory_str] - Theory_limit[Plane_str]).sum() * sample_time / 3600
        text = [wfname, Benchmarking_limit_value, Theory_limit_value]
        text = wfname + '时间：' + start_time[:-4] + '~' + end_time[:-4] + '\n' + '标杆机组法限电:' + str(
            int(Benchmarking_limit_value)) + '度' + '\n理论功率法限电量:' + str(int(Theory_limit_value)) + '度'
        # print(text)
        return wfname, Theory_limit_value
        # return wfname, text, int(Benchmarking_limit_value), int(Theory_limit_value)

    push_info = []
    for i in range(len(data)):
        try:
            wfname, limit_data = get_ration_ele(data['wfname'].iloc[i], data['wtid'].iloc[i], day_num, sample_time)
            if (wfname, limit_data) not in push_info:
                push_info.append((wfname, limit_data))
        except:
            print(data['wfname'].iloc[i])

    # print(push_info)
    kexing_AVC = 410726710
    feature_agc = ['EMSD.PwrAt.Ra.F32.PlannedValue']
    sample_time = 30  # 采样频率30s
    start_time = (datetime.datetime.now() - datetime.timedelta(days=day_num)).strftime("%Y-%m-%d ") + '00:00:00.000'
    end_time = (datetime.datetime.now() - datetime.timedelta(days=day_num - 1)).strftime("%Y-%m-%d ") + '00:00:00.000'
    get_data_EMSD = GH.get_wtid_data(str(int(kexing_AVC)), start_time=start_time, end_time=end_time, sample=sample_time,
                                     info=feature_agc)
    get_data_EMSD.index = get_data_EMSD['time']
    get_data_EMSD_df = get_data_EMSD[feature_agc].resample('1T', label='right', closed='right').mean()

    wt_5 = 410726005
    feature_agc = ['WTUR.PwrAt.Ra.F32.Side']
    feature_agc = ['WTUR.PwrAt.Ra.F32.Theory']
    sample_time = 7  # 采样频率30s
    start_time = (datetime.datetime.now() - datetime.timedelta(days=day_num)).strftime("%Y-%m-%d ") + '00:00:00.000'
    end_time = (datetime.datetime.now() - datetime.timedelta(days=day_num - 1)).strftime("%Y-%m-%d ") + '00:00:00.000'
    get_data_wt_5 = GH.get_wtid_data(str(int(wt_5)), start_time=start_time, end_time=end_time, sample=sample_time,
                                     info=feature_agc)
    get_data_wt_5.index = get_data_wt_5['time']
    get_data_wt_5_df = get_data_wt_5[feature_agc].resample('1T', label='right', closed='right').mean()
    get_data_wt_5_df['WTUR.PwrAt.Ra.F32.Side'] = get_data_wt_5_df[
        'WTUR.PwrAt.Ra.F32.Theory']  #####################################################
    get_data_wt_5_df = get_data_wt_5_df.drop(labels='WTUR.PwrAt.Ra.F32.Theory', axis=1)  ###############

    wt_25 = 410727025
    feature_agc = ['WTUR.PwrAt.Ra.F32']
    # feature_agc=['WTUR.PwrAt.Ra.F32.Theory']
    sample_time = 7  # 采样频率30s
    day_num = 0
    start_time = (datetime.datetime.now() - datetime.timedelta(days=day_num)).strftime("%Y-%m-%d ") + '00:00:00.000'
    end_time = (datetime.datetime.now() - datetime.timedelta(days=day_num - 1)).strftime("%Y-%m-%d ") + '00:00:00.000'
    start_time = (datetime.datetime.now() - datetime.timedelta(days=day_num)).strftime("%Y-%m-%d ") + '00:00:00.000'
    end_time = (datetime.datetime.now() - datetime.timedelta(days=day_num - 1)).strftime("%Y-%m-%d ") + '00:00:00.000'
    get_data_wt_25 = GH.get_wtid_data(str(int(wt_25)), start_time=start_time, end_time=end_time, sample=sample_time,
                                      info=feature_agc)
    get_data_wt_25.index = get_data_wt_25['time']

    get_data_wt_25_df = get_data_wt_25[feature_agc].resample('1T', label='right', closed='right').mean()
    # get_data_wt_25_df['WTUR.PwrAt.Ra.F32']=get_data_wt_25_df['WTUR.PwrAt.Ra.F32.Theory']#####################################################
    # get_data_wt_25_df=get_data_wt_25_df.drop(labels='WTUR.PwrAt.Ra.F32.Theory',axis=1)#######################

    wt_power = pd.merge(get_data_wt_25_df, get_data_wt_5_df, left_on=get_data_wt_25_df.index,
                        right_on=get_data_wt_5_df.index)

    def get_right(a):
        if a < 0:
            a = 0
        return a

    wt_power['WTUR.PwrAt.Ra.F32'] = wt_power['WTUR.PwrAt.Ra.F32'].apply(lambda x: get_right(x))
    wt_power['WTUR.PwrAt.Ra.F32.Side'] = wt_power['WTUR.PwrAt.Ra.F32.Side'].apply(lambda x: get_right(x))

    wt_power['4MW'] = wt_power['WTUR.PwrAt.Ra.F32'] / 4000 * 28000
    wt_power['2.5MW'] = wt_power['WTUR.PwrAt.Ra.F32.Side'] / 2500 * 40000
    wt_power['2.5add4MW'] = (wt_power['4MW'] + wt_power['2.5MW'])
    # wt_power['2.5add4MW']=(wt_power['4MW'])#########
    wt_power['6.5MW'] = (wt_power['WTUR.PwrAt.Ra.F32.Side'] + wt_power['WTUR.PwrAt.Ra.F32']) / 6500 * 68000
    # wt_power['6.5MW']=(wt_power['WTUR.PwrAt.Ra.F32.Side'])/2500*40000
    new = pd.merge(wt_power, get_data_EMSD_df, left_on='key_0', right_on=get_data_EMSD_df.index)
    new = new[new['EMSD.PwrAt.Ra.F32.PlannedValue'] < (68000 * 0.99)]

    Theory_limit_value3 = 0
    if len(new) > 0:

        new2 = new[
            (new['EMSD.PwrAt.Ra.F32.PlannedValue'] < new['2.5add4MW']) & (new['EMSD.PwrAt.Ra.F32.PlannedValue'] > 0)]
        Theory_limit_value2 = (new2['2.5add4MW'] - new2['EMSD.PwrAt.Ra.F32.PlannedValue']).sum() * 60 / 3600

        new3 = new[(new['EMSD.PwrAt.Ra.F32.PlannedValue'] < new['6.5MW']) & (new['EMSD.PwrAt.Ra.F32.PlannedValue'] > 0)]
        Theory_limit_value3 = (new3['6.5MW'] - new3['EMSD.PwrAt.Ra.F32.PlannedValue']).sum() * 60 / 3600
        print(start_time)
        print('2.5add4MW ' + str(Theory_limit_value2))
        print('6.5MW ' + str(Theory_limit_value3))
    else:
        print(start_time)
        print('2.5add4MW ' + str(0))
        print('6.5MW ' + str(0))

    if Theory_limit_value3 > 0:
        start_time = (datetime.datetime.now() - datetime.timedelta(days=day_num)).strftime("%Y-%m-%d ") + '00:00:00.000'
        end_time = (datetime.datetime.now() - datetime.timedelta(days=day_num)).strftime("%Y-%m-%d ") + '23:59:59.000'
        push_data = '---' + '科兴' + '---' + '\n【标杆机组法限电】:' + str(
            int(Theory_limit_value3)) + '   ' + start_time + end_time

        # B = wehat_Info('wu', 'aa', '限电信息')
        push_data_d = '---' + '科兴' + '---' + '\n\n【标杆机组法限电】:' + str(
            int(Theory_limit_value3)) + '   ' + start_time + end_time  ##科兴限功率数据
        # A2=c.token_id['限电信息推送']
        # A1 = DingDingBot.token_id['限电信息推送']
        # DingDingBot.dingmessage(A1, push_data_d)
        push_info.append(('科兴', Theory_limit_value3))

    else:
        push_data_d = '---' + '科兴' + '---' + '\n\n【标杆机组法限电】:' + str(
            int(Theory_limit_value3)) + '   ' + start_time + end_time  ##科兴限功率数据

        push_info.append(('科兴', Theory_limit_value3))

    print(push_info)

    df = pd.DataFrame(push_info, columns=['电场名称', '弃电量'])

    # 显示DataFrame
    wfid_dict = {
        '泉山': '泉山风电场',
        '南阳凯润': '凯润风电场',
        '嘉润': '嘉润风电场',
        '科兴': '科兴风电场',
        '润清': '润清风电场',
        '润金': '润金风电场',
        '雅润': '雅润风电场',
        '驭风(卫南坡)': '驭风风电场',
        '金燕': '金燕风电场',
        '飞翔': '飞翔风电场',

    }
    for k, v in wfid_dict.items():
        df['电场名称'] = df['电场名称'].replace({k: v})
        # 如果泉山在df[电厂名称]中，则修改泉山为泉山风电场

    # 创建新的DataFrame，名称为newsdf
    new_df = df[df['电场名称'].str.contains('风电场')]
    new_df = new_df.drop_duplicates(subset='电场名称')
    print(new_df)
    return new_df
#
# if __name__ == '__main__':
#     qdl_df()
