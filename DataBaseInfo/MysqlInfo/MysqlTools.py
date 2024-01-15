#! /usr/bin/env python
# -*-coding:utf-8-*-
import os
import yaml
import pymysql
import pandas as pd
from LogInfo.LogTools import Logger


class MysqlCurd(object):
    def __init__(self, config_file=None):
        # 读取YAML配置文件
        self.log = Logger()
        config = self.creat_yml(config_file)
        self.host = config['host']
        self.port = config['port']
        self.user = config['username']
        self.password = config['password']
        self.db = config['database']
        self.connection = self.connect()

    def creat_yml(self, yml_config_file):
        '''
        指定yml路径
        :param config_file: yml配置文件路径
        :return:
        '''
        if yml_config_file:
            with open(yml_config_file, 'r') as f:
                config_sql = yaml.safe_load(f)
                self.log.info(F"用户配置sql文件:{yml_config_file}")

        else:
            filename = 'nanfangyunying.yml'
            script_directory = os.path.dirname(os.path.abspath(__file__))
            config_file = os.path.join(script_directory, filename)
            with open(config_file, 'r') as f:
                config_sql = yaml.safe_load(f)
            self.log.info(F"已走默认配置文件:{filename}")

        return config_sql

    def connect(self):
        """连接MySQL数据库"""
        connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db
        )
        self.log.info(F"成功连接数据库:{self.db}")
        return connection

    def close(self):
        """关闭MySQL数据库连接"""
        if self.connection is not None:
            self.connection.close()
            self.connection = None
            self.log.info(F"关闭数据库{self.db}")
    def query_sql(self, sql='select version()'):
        '''
        sql查询数据
        :param sql:  sql 语句
        :return: df
        '''
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        except Exception as e:
            self.log.info(F"请求数据有误:{e}")
            return None
    def query(self, sql='select version()'):
        '''
        sql查询数据
        :param sql:  sql 语句
        :return: df
        '''
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                df = pd.DataFrame(result)
                return df
        except Exception as e:
            self.log.info(F"请求数据有误:{e}")
            return None

    def query_sql_return_header_and_data(self, sql):
        '''
        sql查询数据,返回df带字段名称
        :param sql: sql 语句
        :return:  df
        '''
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                daily_data = cursor.fetchall()
                cursor.close()
                df = pd.DataFrame(daily_data, columns=[i[0] for i in cursor.description])
                return df
        except Exception as e:
            self.log.info(F"请求数据有误:{e}")
            return None

    def query_uk(self):
        '''
        uk 信息查询
        :return:  df(过滤后)
        '''
        try:
            with self.connection.cursor() as cursor:
                sql = 'select * from data_oms_uk'
                cursor.execute(sql)
                daily_data = cursor.fetchall()
                cursor.close()
                df = pd.DataFrame(daily_data, columns=[i[0] for i in cursor.description])
                data = df.loc[
                    df['UK密钥MAC地址'].notnull(),
                    ['场站', 'UK密钥MAC地址', '外网oms账号', '外网oms密码', '是否正常使用']]
                # data = df.loc[
                #     df['UK密钥MAC地址'].notnull() & (df['是否正常使用'] == '是'),
                #     ['场站', 'UK密钥MAC地址', '外网oms账号', '外网oms密码', '是否正常使用']]

                df_filtered = data.drop_duplicates(subset='场站')
                return df_filtered
        except Exception as e:
            self.log.info(F"请求数据有误:{e}")
            return None

    def update(self, sql='select version()'):
        '''
        sql插入数据
        :param sql:  sql 语句
        :return: df
        '''
        try:
            with self.connection.cursor() as cursor:
                result = cursor.execute(sql)
                self.connection.commit()
                cursor.close()
                return F'更新成功,更新{result}条数据'
        except Exception as e:
            self.log.info(F"请求数据有误:{e}")
            return F'更新失败！'

    def insert_list(self,table_name, field_name, field_data):
        # 我们假设MC是一个类似SQLite数据库的连接对象
        # 您需要根据实际情况修改下面的代码


        try:
            with self.connection.cursor() as cursor:
                # 创建插入SQL语句
                fields = ','.join(field_name)
                values = ','.join(['%s'] * len(field_name))
                sql = f"INSERT INTO {table_name} ({fields}) VALUES ({values})"
                # 执行插入操作
                cursor.execute(sql, field_data)
                self.connection.commit()
                cursor.close()
                return F'添加成功,更新{len(field_data)}条数据'
        except Exception as e:
            self.log.info(F"请求数据有误:{e}")
            return F'添加失败！'

    def delete(self, sql='select version()'):
        """
        删除
        """
        try:
            with self.connection.cursor() as cursor:
                result = cursor.execute(sql)
                self.connection.commit()
                cursor.close()
                self.log.info( F'删除更成功,删除{result}条数据')

                return F'删除更成功,删除{result}条数据'
        except Exception as e:
            self.log.info(F"请求数据有误:{e}")
            return F'删除失败！'


# if __name__ == '__main__':
#     MC = MysqlCurd()
# #     res_uk = MC.query_uk()
# # #     sql = F"-- select * from  data_oms   where   日期='2023-09-14' and 电场名称='凯润风电场'"
# # #     sql = F"update   data_oms  set  是否已完成 =8 where 电场名称 ='凯润风电场' and 日期='2023-09-12'"
# # #     res_uk = MC.update(sql)
# #     print(res_uk)
#     sql ="delete from data_sxz_ddgl_bwdyqxkhjg_rhgljg  WHERE check_data ='2023-12-10' and check_wfname='嘉润风电场'"
#     MC.delete(sql)
