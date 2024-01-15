# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 14:51:27 2021

@author: TianRun11
"""


####get_wtid_info返回wtid的所有info
###get_all_wtid 返回所有wtid
###get_wtid_data下采样数据
###get_wtid_single_data 抽取
###Get_info_Hbase_south 南方清丰机房数据库
###Get_info_Hbase_intellect 中心清丰机房数据库
class Get_info_Hbase_south():
    import json
    import requests
    import pandas as pd

    def __init__(self, wtid='', start_time='', end_time='', info=[]):

        self.wtid = wtid
        self.start_time = start_time
        self.end_time = end_time
        self.info = info

    def get_wtid_info(self, wtid):  ###返回wtid下所有测点(100台耗时3s)
        import json
        import requests
        import pandas as pd
        self_wtid = wtid
        headers = {
            'Accept': '*/*',
            'appKey': 'Nltp5EIq5hwTKlHKwgtbnamzAidl3118QXdP44iZJC4=',
        }

        response = requests.get('http://16.3.1.32:8082/meta/getLatestTagsByObjectName/' + self_wtid, headers=headers)
        a_result = json.loads(response.text)
        if len(a_result['data']['tags']) > 0:

            z = a_result['data']['tags'][0]['tagDetail']
            info = []
            for item in z:
                info.append(item['iecpath'])
            info_pd = pd.DataFrame(info)
            info_pd.columns = ['hbase_info']
            info_pd['wtid'] = self_wtid
            info_pd['protocolid'] = a_result['data']['tags'][0]['protocolID']
        else:
            info_pd = []
        return info_pd

    def get_all_wtid(self):  ###返回wtid所有点位(100台耗时3s)
        import json
        import requests
        import pandas as pd

        headers = {
            'Accept': '*/*',
            'appKey': 'Nltp5EIq5hwTKlHKwgtbnamzAidl3118QXdP44iZJC4=',
        }

        response = requests.get('http://16.3.1.32:8082/meta/getObjectNamesByNameFilter', headers=headers)

        a_result = json.loads(response.text)
        if len(a_result['data']) > 0:
            info_pd = pd.DataFrame(a_result['data'])
            info_pd.columns = ['wtid']
        else:
            info_pd = []
        return info_pd

    def get_wtid_data(self, wtid, start_time='2021-12-11 06:54:25.000', end_time='2021-12-16 06:54:25.000', sample=7,
                      info=[]):  # info是字段名，必须以list形式，sample是下采样频率，单位s
        import json
        import requests
        import pandas as pd
        sample = sample * 1000
        if len(start_time) < 20 and len(start_time) > 15:
            start_time = start_time + '.100'
        if len(end_time) < 20 and len(end_time) > 15:
            start_time = start_time + '.100'

        def TimepStamp(var):
            import datetime
            timeStamp = var / 1000
            dateArray = datetime.datetime.fromtimestamp(timeStamp)
            return dateArray

        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'appKey': 'Nltp5EIq5hwTKlHKwgtbnamzAidl3118QXdP44iZJC4=',
        }
        tags = {wtid: info}
        data = {"compress": 'true',
                "dataCategory": "REALDATA",
                "endTime": end_time,
                "interval": sample,
                "offsetInterval": 0,
                "startTime": start_time,
                "tags": tags}

        data = str(data).replace('\'true\'', 'true')
        data = str(data).replace('\'', '\"')
        response = requests.post('http://16.3.1.32:8082/query/getDataByTimeSpan', headers=headers, data=data)
        a_result = json.loads(response.text)
        if len(a_result['data']) > 0 and a_result['status'] == 'OK':
            time = a_result['data']['timeCollect'][0]['timeList']
            wt_data = pd.DataFrame(time)
            wt_data.columns = ['time']
            wt_data['time'] = wt_data['time'].apply(lambda x: TimepStamp(x))
            value = a_result['data']['tagValueListMap']
            for item in list(value.keys()):
                item_name = item[item.find('.') + 1:]
                item_value = value[item]['valueList']
                item_value = pd.DataFrame(item_value)
                item_value.columns = [item_name]
                wt_data = pd.concat([wt_data, item_value], axis=1)
        else:
            wt_data = []
        return wt_data

    def get_wtid_single_data(self, wtid, start_time='', info=[]):  # info是字段名，获得指定时间的单条数据,默认最多半小时前
        import json
        import requests
        import pandas as pd
        import datetime
        if len(start_time) < 20 and len(start_time) > 15:
            start_time = start_time + '.100'

        def TimepStamp(var):

            timeStamp = var / 1000
            dateArray = datetime.datetime.fromtimestamp(timeStamp)
            return dateArray

        if len(start_time) == 0:
            start_time = (datetime.datetime.now() - datetime.timedelta(seconds=240)).strftime(
                "%Y-%m-%d %H:%M:%S") + '.000'

        for i in range(10):

            headers = {
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'appKey': 'Nltp5EIq5hwTKlHKwgtbnamzAidl3118QXdP44iZJC4=',
            }
            tags = {wtid: info}
            data = {"compress": 'true',
                    "dataCategory": "REALDATA",
                    "startTime": start_time,
                    "tags": tags}

            data = str(data).replace('\'true\'', 'true')
            data = str(data).replace('\'', '\"')
            response = requests.post('http://16.3.1.32:8082/query/getSingleData', headers=headers, data=data)
            a_result = json.loads(response.text)
            start_time = (datetime.datetime.now() - datetime.timedelta(seconds=240 + (i + 1) * 180)).strftime(
                "%Y-%m-%d %H:%M:%S") + '.000'
            if len(a_result['data']['relaMap']) > 0:
                break

        if len(a_result['data']['relaMap']) > 0 and a_result['status'] == 'OK':
            time = a_result['data']['timeCollect'][0]['timeList']
            wt_data = pd.DataFrame(time)
            wt_data.columns = ['time']
            wt_data['time'] = wt_data['time'].apply(lambda x: TimepStamp(x))
            value = a_result['data']['tagValueListMap']
            for item in list(value.keys()):
                item_name = item[item.find('.') + 1:]
                item_value = value[item]['valueList']
                item_value = pd.DataFrame(item_value)
                item_value.columns = [item_name]
                wt_data = pd.concat([wt_data, item_value], axis=1)
                wt_data['wtid'] = wtid
        else:
            wt_data = []
        return wt_data

    def get_wtid_change_data(self, wtid, info=[]):  # info是字段名，获得指定时间的单条数据,默认最多半小时前,info只能输入单个值
        import json
        import requests
        import pandas as pd
        import datetime

        def TimepStamp(var):

            timeStamp = var / 1000
            dateArray = datetime.datetime.fromtimestamp(timeStamp)
            return dateArray

        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'appKey': 'Nltp5EIq5hwTKlHKwgtbnamzAidl3118QXdP44iZJC4=',
        }
        tags = {wtid: info}
        data = {"compress": 'true',
                "dataCategory": "CHANGESAVE",
                "tags": tags}

        data = str(data).replace('\'true\'', 'true')
        data = str(data).replace('\'', '\"')
        response = requests.post('http://16.3.1.32:8082/query/getSectionData', headers=headers, data=data)
        a_result = json.loads(response.text)

        if len(a_result['data']['relaMap']) > 0 and a_result['status'] == 'OK':
            time = a_result['data']['timeCollect'][0]['timeList']
            wt_data = pd.DataFrame(time)
            wt_data.columns = ['time']
            wt_data['time'] = wt_data['time'].apply(lambda x: TimepStamp(x))
            value = a_result['data']['tagValueListMap']

            for item in list(value.keys()):
                time = a_result['data']['timeCollect'][0]['timeList']
                wt_data = pd.DataFrame(time)
                wt_data.columns = ['time']
                wt_data['time'] = wt_data['time'].apply(lambda x: TimepStamp(x))
                value = a_result['data']['tagValueListMap']
                item_name = item[item.find('.') + 1:]
                item_value = value[item]['valueList']
                item_value = pd.DataFrame(item_value)
                item_value.columns = ['change_data']
                item_value['info'] = [item_name]
                if item == list(value.keys())[0]:
                    wt_data = pd.concat([wt_data, item_value], axis=1)
                wt_data['wtid'] = wtid
        else:
            wt_data = []
        return wt_data

    def get_wtid_trend_data(self, wtid, start_time='2021-12-11 06:54:25.000', end_time='2021-12-16 06:54:25.000',
                            sample=7200, info=[]):  # info是字段名，必须以list形式，趋势间隔，单位s
        import json
        import requests
        import pandas as pd
        sample = sample * 1000
        if len(start_time) < 20 and len(start_time) > 15:
            start_time = start_time + '.100'
        if len(end_time) < 20 and len(end_time) > 15:
            start_time = start_time + '.100'

        def TimepStamp(var):
            import datetime
            timeStamp = var / 1000
            dateArray = datetime.datetime.fromtimestamp(timeStamp)
            return dateArray

        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'appKey': 'Nltp5EIq5hwTKlHKwgtbnamzAidl3118QXdP44iZJC4=',
        }
        tags = {wtid: info}
        data = {"compress": 'true',
                "dataCategory": "REALDATA",
                "endTime": end_time,
                "interval": sample,
                "offsetInterval": 0,
                "startTime": start_time,
                "tags": tags}

        data = str(data).replace('\'true\'', 'true')
        data = str(data).replace('\'', '\"')
        response = requests.post('http://16.3.1.32:8082/query/getTrendData', headers=headers, data=data)
        a_result = json.loads(response.text)
        if len(a_result['data']['relaMap']) > 0 and a_result['status'] == 'OK':
            time = a_result['data']['timeCollect'][1]['timeList']
            wt_data = pd.DataFrame(time)
            wt_data.columns = ['time']
            wt_data['time'] = wt_data['time'].apply(lambda x: TimepStamp(x))
            value = a_result['data']['tagValueListMap']
            for item in list(value.keys()):
                item_name = item[item.find('.') + 1:]
                item_value = value[item]['valueList']
                item_value = pd.DataFrame(item_value)
                item_value.columns = [item_name]
                wt_data = pd.concat([wt_data, item_value], axis=1)
        else:
            wt_data = []
        return wt_data


class Get_info_Hbase_intellect():
    import json
    import requests
    import pandas as pd

    def __init__(self, wtid='', start_time='', end_time='', info=[]):

        self.wtid = wtid
        self.start_time = start_time
        self.end_time = end_time
        self.info = info

    def get_wtid_info(self, wtid):  ###返回wtid下所有测点(100台耗时3s)
        import json
        import requests
        import pandas as pd
        self_wtid = wtid
        headers = {
            'Accept': '*/*',
            'appKey': 'HLutl21rHUI0aSkRWWvLJ5/KPEFOR7BsSXCtfztL1UM=',
        }

        response = requests.get('http://10.12.27.3:8082/meta/getLatestTagsByObjectName/' + self_wtid, headers=headers)
        a_result = json.loads(response.text)
        if len(a_result['data']['tags']) > 0:

            z = a_result['data']['tags'][0]['tagDetail']
            info = []
            for item in z:
                info.append(item['iecpath'])
            info_pd = pd.DataFrame(info)
            info_pd.columns = ['hbase_info']
            info_pd['wtid'] = self_wtid
            info_pd['protocolid'] = a_result['data']['tags'][0]['protocolID']
        else:
            info_pd = []
        return info_pd

    def get_all_wtid(self):  ###返回wtid所有点位(100台耗时3s)
        import json
        import requests
        import pandas as pd

        headers = {
            'Accept': '*/*',
            'appKey': 'HLutl21rHUI0aSkRWWvLJ5/KPEFOR7BsSXCtfztL1UM=',
        }

        response = requests.get('http://10.12.27.3:8082/meta/getObjectNamesByNameFilter', headers=headers)

        a_result = json.loads(response.text)
        if len(a_result['data']) > 0:
            info_pd = pd.DataFrame(a_result['data'])
            info_pd.columns = ['wtid']
        else:
            info_pd = []
        return info_pd

    def get_wtid_data(self, wtid, start_time='2021-12-11 06:54:25.000', end_time='2021-12-16 06:54:25.000', sample=7,
                      info=[]):  # info是字段名，必须以list形式，sample是下采样频率，单位s
        import json
        import requests
        import pandas as pd
        sample = sample * 1000
        if len(start_time) < 20 and len(start_time) > 15:
            start_time = start_time + '.100'
        if len(end_time) < 20 and len(end_time) > 15:
            start_time = start_time + '.100'

        def TimepStamp(var):
            import datetime
            timeStamp = var / 1000
            dateArray = datetime.datetime.fromtimestamp(timeStamp)
            return dateArray

        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'appKey': 'HLutl21rHUI0aSkRWWvLJ5/KPEFOR7BsSXCtfztL1UM=',
        }
        tags = {wtid: info}
        data = {"compress": 'true',
                "dataCategory": "REALDATA",
                "endTime": end_time,
                "interval": sample,
                "offsetInterval": 0,
                "startTime": start_time,
                "tags": tags}

        data = str(data).replace('\'true\'', 'true')
        data = str(data).replace('\'', '\"')
        response = requests.post('http://10.12.27.3:8082/query/getDataByTimeSpan', headers=headers, data=data)
        a_result = json.loads(response.text)
        if len(a_result['data']) > 0 and a_result['status'] == 'OK':
            time = a_result['data']['timeCollect'][0]['timeList']
            wt_data = pd.DataFrame(time)
            wt_data.columns = ['time']
            wt_data['time'] = wt_data['time'].apply(lambda x: TimepStamp(x))
            value = a_result['data']['tagValueListMap']
            for item in list(value.keys()):
                item_name = item[item.find('.') + 1:]
                item_value = value[item]['valueList']
                item_value = pd.DataFrame(item_value)
                item_value.columns = [item_name]
                wt_data = pd.concat([wt_data, item_value], axis=1)
        else:
            wt_data = []
        return wt_data

    def get_wtid_single_data(self, wtid, start_time='', info=[]):  # info是字段名，获得指定时间的单条数据,默认最多半小时前
        import json
        import requests
        import pandas as pd
        import datetime
        if len(start_time) < 20 and len(start_time) > 15:
            start_time = start_time + '.100'

        def TimepStamp(var):

            timeStamp = var / 1000
            dateArray = datetime.datetime.fromtimestamp(timeStamp)
            return dateArray

        if len(start_time) == 0:
            start_time = (datetime.datetime.now() - datetime.timedelta(seconds=240)).strftime(
                "%Y-%m-%d %H:%M:%S") + '.000'

        for i in range(10):

            headers = {
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'appKey': 'HLutl21rHUI0aSkRWWvLJ5/KPEFOR7BsSXCtfztL1UM=',
            }
            tags = {wtid: info}
            data = {"compress": 'true',
                    "dataCategory": "REALDATA",
                    "startTime": start_time,
                    "tags": tags}

            data = str(data).replace('\'true\'', 'true')
            data = str(data).replace('\'', '\"')
            response = requests.post('http://10.12.27.3:8082/query/getSingleData', headers=headers, data=data)
            a_result = json.loads(response.text)
            start_time = (datetime.datetime.now() - datetime.timedelta(seconds=240 + (i + 1) * 180)).strftime(
                "%Y-%m-%d %H:%M:%S") + '.000'
            if len(a_result['data']['relaMap']) > 0:
                break

        if len(a_result['data']['relaMap']) > 0 and a_result['status'] == 'OK':
            time = a_result['data']['timeCollect'][0]['timeList']
            wt_data = pd.DataFrame(time)
            wt_data.columns = ['time']
            wt_data['time'] = wt_data['time'].apply(lambda x: TimepStamp(x))
            value = a_result['data']['tagValueListMap']
            for item in list(value.keys()):
                item_name = item[item.find('.') + 1:]
                item_value = value[item]['valueList']
                item_value = pd.DataFrame(item_value)
                item_value.columns = [item_name]
                wt_data = pd.concat([wt_data, item_value], axis=1)
                wt_data['wtid'] = wtid
        else:
            wt_data = []
        return wt_data

    def get_wtid_change_data(self, wtid, info=[]):  # info是字段名，获得指定时间的单条数据,默认最多半小时前,info只能输入单个值
        import json
        import requests
        import pandas as pd
        import datetime

        def TimepStamp(var):

            timeStamp = var / 1000
            dateArray = datetime.datetime.fromtimestamp(timeStamp)
            return dateArray

        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'appKey': 'HLutl21rHUI0aSkRWWvLJ5/KPEFOR7BsSXCtfztL1UM=',
        }
        tags = {wtid: info}
        data = {"compress": 'true',
                "dataCategory": "CHANGESAVE",
                "tags": tags}

        data = str(data).replace('\'true\'', 'true')
        data = str(data).replace('\'', '\"')
        response = requests.post('http://10.12.27.3:8082/query/getSectionData', headers=headers, data=data)
        a_result = json.loads(response.text)

        if len(a_result['data']['relaMap']) > 0 and a_result['status'] == 'OK':
            time = a_result['data']['timeCollect'][0]['timeList']
            wt_data = pd.DataFrame(time)
            wt_data.columns = ['time']
            wt_data['time'] = wt_data['time'].apply(lambda x: TimepStamp(x))
            value = a_result['data']['tagValueListMap']

            for item in list(value.keys()):
                time = a_result['data']['timeCollect'][0]['timeList']
                wt_data = pd.DataFrame(time)
                wt_data.columns = ['time']
                wt_data['time'] = wt_data['time'].apply(lambda x: TimepStamp(x))
                value = a_result['data']['tagValueListMap']
                item_name = item[item.find('.') + 1:]
                item_value = value[item]['valueList']
                item_value = pd.DataFrame(item_value)
                item_value.columns = ['change_data']
                item_value['info'] = [item_name]
                if item == list(value.keys())[0]:
                    wt_data = pd.concat([wt_data, item_value], axis=1)
                wt_data['wtid'] = wtid
        else:
            wt_data = []
        return wt_data

    def get_wtid_trend_data(self, wtid, start_time='2022-10-11 06:54:25.000', end_time='2022-10-16 06:54:25.000',
                            sample=7200, info=[]):  # info是字段名，必须以list形式，趋势间隔，单位s
        import json
        import requests
        import pandas as pd
        sample = sample * 1000
        if len(start_time) < 20 and len(start_time) > 15:
            start_time = start_time + '.100'
        if len(end_time) < 20 and len(end_time) > 15:
            start_time = start_time + '.100'

        def TimepStamp(var):
            import datetime
            timeStamp = var / 1000
            dateArray = datetime.datetime.fromtimestamp(timeStamp)
            return dateArray

        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'appKey': 'HLutl21rHUI0aSkRWWvLJ5/KPEFOR7BsSXCtfztL1UM=',
        }
        tags = {wtid: info}
        data = {"compress": 'true',
                "dataCategory": "REALDATA",
                "endTime": end_time,
                "interval": sample,
                "offsetInterval": 0,
                "startTime": start_time,
                "tags": tags}

        data = str(data).replace('\'true\'', 'true')
        data = str(data).replace('\'', '\"')
        response = requests.post('http://10.12.27.3:8082/query/getTrendData', headers=headers, data=data)
        a_result = json.loads(response.text)
        if len(a_result['data']['relaMap']) > 0 and a_result['status'] == 'OK':
            time = a_result['data']['timeCollect'][1]['timeList']
            wt_data = pd.DataFrame(time)
            wt_data.columns = ['time']
            wt_data['time'] = wt_data['time'].apply(lambda x: TimepStamp(x))
            value = a_result['data']['tagValueListMap']
            for item in list(value.keys()):
                item_name = item[item.find('.') + 1:]
                item_value = value[item]['valueList']
                item_value = pd.DataFrame(item_value)
                item_value.columns = [item_name]
                wt_data = pd.concat([wt_data, item_value], axis=1)
        else:
            wt_data = []
        return wt_data

if __name__ == '__main__':
    pass