# 使用列表表达式生成8个空值的列表

i = 3
uuid_num = 12


def check_data_report(i, uuid_num):
    from DataBaseInfo.MysqlInfo.MysqlTools import MysqlCurd

    new_nanfang = F'../DataBaseInfo/MysqlInfo/new_nanfang.yml'
    Mc = MysqlCurd(new_nanfang)
    sql = F"select  场站 from data_oms_uk  where usb序号='{i}' and uuid ='{uuid_num}'   "
    wfname = Mc.query_sql(sql)[0][0]
    import datetime

    yes_day = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    sql_ = F"select  是否已完成 from data_oms  where 电场名称='{wfname}' and 日期 ='{yes_day}'   "
    print(sql_)
    num = Mc.query_sql(sql_)[0][0]
    return num


print(check_data_report(i, uuid_num))
