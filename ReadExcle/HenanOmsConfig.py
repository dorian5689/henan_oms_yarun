# henan_oms_config = """
# SELECT  a.电场名称, a.日期, a.发电量, a.上网电量, round(a.弃电量/10000,4) 弃电量, b.储能最大充电电力, b.储能最大放电电力, b.储能日充电, b.储能日放电, b.充电次数, b.放电次数, a.填报开始时间, a.填报结束时间, case  when a.是否已完成 = 1 then '已填报' else '未填报' end 是否已完成
# FROM nanfangyunying.data_oms a
# left join nanfangyunying.data_oms_c b
# on a.电场名称=b.电场名称 and a.日期=b.日期
# where STR_TO_DATE(a.日期, '%Y-%m-%d')>=current_date()-1
# """


henan_oms_config ="""

SELECT 
    a.电场名称, 
    a.日期, 
    a.发电量, 
    a.上网电量, 
    ROUND(a.弃电量/10000, 4) AS 弃电量, 
    b.储能最大充电电力, 
    b.储能最大放电电力, 
    b.储能日充电, 
    b.储能日放电, 
    b.充电次数, 
    b.放电次数, 
    a.填报开始时间, 
    a.填报结束时间, 
    CASE 
        WHEN a.是否已完成 = 1 THEN '已填报' 
        ELSE '未填报' 
    END AS 是否已完成
FROM nanfangyunying.data_oms a
LEFT JOIN nanfangyunying.data_oms_c b
ON a.电场名称=b.电场名称 AND a.日期=b.日期
WHERE a.日期 >= CURDATE() - INTERVAL 1 DAY;
"""

henan_oms_config_new ="""

SELECT 
    a.电场名称, 
    a.日期, 
    a.发电量, 
    a.上网电量, 
    ROUND(a.弃电量/10000, 4) AS 弃电量, 
    b.储能最大充电电力, 
    b.储能最大放电电力, 
    b.储能日充电, 
    b.储能日放电, 
    b.充电次数, 
    b.放电次数, 
    a.填报开始时间, 
    a.填报结束时间, 
    CASE 
        WHEN a.是否已完成 = 1 THEN '已填报' 
        ELSE '未填报' 
    END AS 是否已完成
FROM nanfang.data_oms a
LEFT JOIN nanfang.data_oms_c b
ON a.电场名称=b.电场名称 AND a.日期=b.日期
WHERE a.日期 >= CURDATE() - INTERVAL 1 DAY;
"""
