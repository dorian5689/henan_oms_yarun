#! /usr/bin/env python
# -*-coding:utf-8-*-
import os
import time
import xlwt
import psycopg2
import datetime
import pandas as pd
import numpy as np
import schedule
from sqlalchemy import create_engine
from DingInfo.DingtalkBot import DingapiTools

print('oms河南区域每日发送')

save_data = datetime.datetime.now().strftime("%Y-%m-%d")


def runtask():
    hh3 = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
    hh4 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
    # hh3 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
    # hh4 = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d 00:00:00')

    conn = psycopg2.connect(database="v5", user="tradmin", password="trxn@2019", host="16.3.1.22", port="8101")
    print("成功")
    cursor = conn.cursor()
    from HenanSqlConfig import henansql
    cursor.execute(henansql, (hh4, hh3))
    daily_data = cursor.fetchall()
    cols = cursor.description
    cursor.close()
    conn.close()
    col = []
    for i in cols:
        col.append(i[0])

    df = pd.DataFrame(daily_data, columns=col)[['省份', '电场名称', '日期', '发电量', '上网电量']]
    try:
        from DataBaseInfo.qdl import qdl_df
        newdf = qdl_df()
        merged_df = pd.merge(df, newdf, on='电场名称', how='left')
        merged_df["弃电量"] = merged_df["弃电量"].fillna(0)
        merged_df["弃电量"] = merged_df["弃电量"].astype(int)
    except Exception as e:
        merged_df = df

    merged_df.to_excel('河南oms.xlsx')

    # password = f"xzy@1234"
    # from urllib import parse
    # password = parse.quote_plus(password)
    # engine = create_engine(
    #     F'mysql+pymysql://xuzhiyong:{password}@rm-2zej7q7186wi4eds5no.mysql.rds.aliyuncs.com:3306/nanfangyunying')
    # # 将数据转换为MySQL数据库可以存储的格式
    try:
        from AutoLogin.DataBaseInfo.MysqlInfo.MysqlTools import MysqlCurd
        MC = MysqlCurd()
        for index, row in merged_df.iterrows():
            sf = row["省份"]
            dcmc = row["电场名称"]
            rq = row["日期"]
            fdl = row["发电量"]
            swdl = row["上网电量"]
            try:
                qdl = row["弃电量"]
            except:
                qdl = 0
            insert_sql = F"INSERT INTO data_oms (省份,电场名称,日期,发电量,上网电量,弃电量) VALUES ('{sf}','{dcmc}','{rq}','{fdl}','{swdl}','{qdl}')"
            update_sql = F" UPDATE data_oms SET 发电量= '{fdl}', 上网电量 = '{swdl}',  弃电量= '{qdl}' WHERE 电场名称= '{dcmc}' and 日期 ='{rq}' "
            check_sql = F"select count(*) from data_oms where 电场名称 ='{dcmc}' and  日期 = '{rq}' "
            result_oms_data1 = MC.query(check_sql)
            result_oms_data = result_oms_data1.values.tolist()[0][0]
            if result_oms_data:
                MC.update(update_sql)
            else:
                MC.update(insert_sql)
            # if MC.update(insert_sql):
            #     print("插入成功")
            # else:
            #     MC.update(update_sql)
            #     print("更新成功")
        # merged_df.to_sql('data_oms', engine, if_exists='append', index=False)
        # merged_df.to_sql('data_oms', engine, if_exists='replace', index=False)
        # 推动到钉钉
        token = "c8eb8d7b8fe2a3c07843233bf225082126db09ab59506bd5631abef4304da29e"
        markdown_true = {
            "title": "推送-数据入库",
            "text": F"OMS数据已经入库,<br>入库时间为<br>{save_data}"}
        DT = DingapiTools()
        DT.SendMessageDing(token, markdown_true)
    except Exception as e:
        print(e)


# runtask()

if __name__ == '__main__':

    print(F'数据推送程序运行中,请勿关闭')
    schedule.every().day.at("00:02").do(runtask)
    while True:
        schedule.run_pending()
        time.sleep(1)
