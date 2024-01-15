# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:46:34 2020

@author: 51613
"""


class my_database:  ##读取数据库

    def real_pg_amsdb(sql):  ###读取V5数据库
        import psycopg2
        import pandas as pd
        conn = psycopg2.connect(database="amsdb", user="ams_ro", password="Ams1212ro2019", host="10.12.1.106",
                                port="5432")
        # print("成功")
        cursor = conn.cursor()
        cursor.execute(sql)
        daily_data = cursor.fetchall()
        des = cursor.description
        daily_data_name = []
        for i in range(len(des)):
            daily_data_name.append(des[i][0])
        daily_data = pd.DataFrame(daily_data)
        if len(daily_data) > 0:
            daily_data.columns = daily_data_name
        cursor.close()
        conn.close()
        return daily_data

    def real_oracle(sql):  ##EAM数据库
        import os
        import pandas as pd
        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
        import cx_Oracle
        conn = cx_Oracle.connect('nfsjfx', 'nfsjfx', '10.12.2.177:1521/maximo')
        cursor = conn.cursor()
        cursor.execute(sql)
        daily_data = cursor.fetchall()
        des = cursor.description
        daily_data_name = []
        for i in range(len(des)):
            daily_data_name.append(des[i][0])
        daily_data = pd.DataFrame(daily_data)
        if len(daily_data) > 0:
            daily_data.columns = daily_data_name
        cursor.close()
        conn.close()
        return daily_data

    def real_mysql_nanfangshuju(sql):  ##读取nanfang mysql库
        import pymysql
        import pandas as pd
        conn = pymysql.connect(
            host="10.12.25.23",  # 主机名
            user="nanfangshuju",  # 用户名
            passwd="acPJ5LpGj3jB8e4K",  # 密码
            db="nanfangshuju")
        cursor = conn.cursor()
        cursor.execute(sql)
        daily_data = cursor.fetchall()
        des = cursor.description
        daily_data_name = []
        try:
            for i in range(len(des)):
                daily_data_name.append(des[i][0])
            daily_data = pd.DataFrame(daily_data)
            if len(daily_data) > 0:
                daily_data.columns = daily_data_name
            cursor.close()
            conn.close()
        except:
            pass
        return daily_data

    def real_sqlite3(sql):  ##读取nanfang mysql库
        import sqlite3
        import pandas as pd
        conn = sqlite3.connect("localdb.sqlite")
        cursor = conn.cursor()
        cursor.execute(sql)
        daily_data = cursor.fetchall()
        des = cursor.description
        daily_data_name = []
        try:

            for i in range(len(des)):
                daily_data_name.append(des[i][0])
            daily_data = pd.DataFrame(daily_data)
            if len(daily_data) > 0:
                daily_data.columns = daily_data_name
            cursor.close()
            conn.close()
        except:
            pass
        return daily_data

    def real_mysql(sql):  ##读取nanfang mysql库
        import pymysql
        import pandas as pd
        conn = pymysql.connect(
            host="rm-2zej7q7186wi4eds5no.mysql.rds.aliyuncs.com",  # 主机名
            user="xuzhiyong",  # 用户名
            passwd="xzy@1234",  # 密码
            db="nanfangyunying")
        cursor = conn.cursor()
        cursor.execute(sql)
        daily_data = cursor.fetchall()
        des = cursor.description
        daily_data_name = []
        try:

            for i in range(len(des)):
                daily_data_name.append(des[i][0])
            daily_data = pd.DataFrame(daily_data)
            if len(daily_data) > 0:
                daily_data.columns = daily_data_name
            cursor.close()
            conn.close()
        except:
            pass

        return daily_data

    def real_pg(sql):  ###读取V5数据库
        import psycopg2
        import pandas as pd
        conn = psycopg2.connect(database="v5", user="tradmin", password="trxn@2019", host="16.3.1.22", port="8101")
        # print("成功")
        cursor = conn.cursor()
        cursor.execute(sql)
        daily_data = cursor.fetchall()
        des = cursor.description
        daily_data_name = []
        for i in range(len(des)):
            daily_data_name.append(des[i][0])
        daily_data = pd.DataFrame(daily_data)
        if len(daily_data) > 0:
            daily_data.columns = daily_data_name
        cursor.close()
        conn.close()
        return daily_data

    def real_pg_tianrun(sql):  ###读取V5数据库
        import psycopg2
        import pandas as pd
        conn = psycopg2.connect(database="tianrun", user="postgres", password="postgres", host="10.12.25.4",
                                port="8101")
        # print("成功")
        cursor = conn.cursor()
        cursor.execute(sql)
        daily_data = cursor.fetchall()
        des = cursor.description
        daily_data_name = []
        for i in range(len(des)):
            daily_data_name.append(des[i][0])
        daily_data = pd.DataFrame(daily_data)
        if len(daily_data) > 0:
            daily_data.columns = daily_data_name
        cursor.close()
        conn.close()
        return daily_data

    def real_pg_ziguan(sql):  ###读取V5数据库
        import psycopg2
        import pandas as pd
        conn = psycopg2.connect(database="DW", user="center_user", password="Tr!123",
                                host="kns-tianrun.cmwyyp2qd6fi.rds.cn-northwest-1.amazonaws.com.cn", port="5432")
        # print("成功")
        cursor = conn.cursor()
        cursor.execute(sql)
        daily_data = cursor.fetchall()
        des = cursor.description
        daily_data_name = []
        for i in range(len(des)):
            daily_data_name.append(des[i][0])
        daily_data = pd.DataFrame(daily_data)
        if len(daily_data) > 0:
            daily_data.columns = daily_data_name
        cursor.close()
        conn.close()
        return daily_data

    def uploda_nanfangshuju(up_data, table_name,
                            up_type):  ###上传数据到nanfangshuju服务器，up_data数据pandas,table_name表命,up_type更新还是替换

        from sqlalchemy import create_engine
        engine = create_engine(
            'mysql+pymysql://nanfangshuju:acPJ5LpGj3jB8e4K@10.12.25.23/nanfangshuju')
        con = engine.connect()
        try:
            up_data.to_sql(table_name, con=engine, index=False, if_exists=up_type)
        except:
            pass
        finally:
            con.close()

    def real_api_eam(sql):  ###读取eam_api
        import pandas as pd
        from urllib import parse
        import json, urllib
        import urllib.request
        from urllib.parse import urlencode
        url_base = '''https://kong.gw-greenenergy.com/select/db_ledger_online?apikey=9A6ptzZMPEmD3jk4PXDOEU4TdeMFFSz4&page=1&pageSize=10000&select='''
        from urllib import parse
        new_url = urllib.request.quote(sql)
        new_url.replace('%25', '%')
        # print(new_url)
        url_base = url_base + new_url
        f = urllib.request.urlopen(url_base)
        nowapi_call = f.read()
        a_result = json.loads(nowapi_call)

        a = pd.read_json(nowapi_call)
        a2 = pd.json_normalize(a_result['list'])
        return a2

    def real_api_eam_db_ledger_online(sql):  ###读取eam_api
        import pandas as pd
        from urllib import parse
        import json, urllib
        import urllib.request
        from urllib.parse import urlencode
        url_base = '''https://kong.gw-greenenergy.com/select/db_ledger_online?apikey=9A6ptzZMPEmD3jk4PXDOEU4TdeMFFSz4&page=1&pageSize=10000&select='''
        from urllib import parse
        new_url = urllib.request.quote(sql)
        new_url.replace('%25', '%')
        # print(new_url)
        url_base = url_base + new_url
        f = urllib.request.urlopen(url_base)
        nowapi_call = f.read()
        a_result = json.loads(nowapi_call)

        a = pd.read_json(nowapi_call)
        a2 = pd.json_normalize(a_result['list'])
        return a2
