henansql = '''
--   雅润、韬润、润清、泉山、凯润、科兴、润金、驭风、嘉润，缺少凯润、科兴
-- 河南豫南
select
    '河南省' 省份,
    CASE WHEN aa.wfid=411328 THEN '泉山风电场'
    WHEN aa.wfid=411311 then '嘉润风电场' 
    WHEN aa.wfid=411335 then '凯润风电场' END 电场名称 ,

	round(aa.QOFC/10000 ,4) 发电量, 
	round(cc.OGC/10000,4) 上网电量,
	to_char(current_date -1 ,'yyyy-mm-dd')  日期

FROM (select
  wfid , sum("WTUR.TotEgyAt.Wt.F32[max]"-"WTUR.TotEgyAt.Wt.F32[min]") QOFC
FROM public.statisticdata_view_0
WHERE wfid IN (411328,411311,411335)
        AND rectime > to_timestamp(concat(to_char(current_date-2,'yyyy-mm-dd') ,' 23:50:00'),'yyyy-MM-dd hh24:mi:ss')
        AND rectime <= to_timestamp(concat(to_char(current_date-1,'yyyy-mm-dd') ,' 23:50:00'),'yyyy-MM-dd hh24:mi:ss')
GROUP BY 
 wfid     ) aa

LEFT JOIN (select
 wfid , SUM("MH.TotEgyAt.Wt.F32.OZ[max]"-"MH.TotEgyAt.Wt.F32.OZ[min]") OGC
FROM public.statisticdata_view_11
WHERE wtid IN (411328801,411311850,411335801)
        AND rectime > to_timestamp(concat(to_char(current_date-2,'yyyy-mm-dd') ,' 23:50:00'),'yyyy-MM-dd hh24:mi:ss')
        AND rectime <= to_timestamp(concat(to_char(current_date-1,'yyyy-mm-dd') ,' 23:50:00'),'yyyy-MM-dd hh24:mi:ss')
GROUP BY 
 wfid  ) cc
    ON aa.wfid=cc.wfid

union all

---- 河南豫北
select
    '河南省' 省份,

    case
        when aa.wfid = 410922 then '润清风电场'
        when aa.wfid = 410901 then '雅润风电场'
        when aa.wfid = 410526 then '润金风电场'
        when aa.wfid = 410923 then '韬润风电场'  
        when aa.wfid = 410728 then '泽润风电场'
		when aa.wfid = 410546 then '驭风风电场'

        WHEN aa.wfid= 411101  then '飞翔风电场'
        WHEN aa.wfid= 410402  then '金燕风电场' end 电场名称 ,
	round(aa.QOFC / 10000 , 4) 发电量,
    round(cc.OGC / 10000, 4) 上网电量,
	to_char(current_date -1 ,'yyyy-mm-dd')  日期

from
    (
    select
        case
            when wfid = 370182 then 370181
            else wfid
        end wfid , sum("WTUR.TotEgyAt.Wt.F32[max]"-"WTUR.TotEgyAt.Wt.F32[min]") QOFC
    from
        public.statisticdata_view_0
    where
        wfid in (410922, 410901, 410526, 410923,410728,410546,411101,410402)
        and rectime > to_timestamp(concat(to_char(current_date-2, 'yyyy-mm-dd') , ' 23:50:00'), 'yyyy-MM-dd hh24:mi:ss')
        and rectime <= to_timestamp(concat(to_char(current_date-1, 'yyyy-mm-dd') , ' 23:50:00'), 'yyyy-MM-dd hh24:mi:ss')
    group by
        case
            when wfid = 370182 then 370181
            else wfid
        end ) aa
left join (
    select
        wfid
        , case
            when wfid = 410901 then ogc-(
            select
                sum("MH.TotEgyAt.Wt.F32.OZ[max]"-"MH.TotEgyAt.Wt.F32.OZ[min]") OGC
            from
                public.statisticdata_view_11
            where
                wtid in (410901813)
                and rectime > to_timestamp(concat(to_char(current_date-2, 'yyyy-mm-dd') , ' 23:50:00'), 'yyyy-MM-dd hh24:mi:ss')
                and rectime <= to_timestamp(concat(to_char(current_date-1, 'yyyy-mm-dd') , ' 23:50:00'), 'yyyy-MM-dd hh24:mi:ss') )
            else ogc
        end ogc
    from
        (
        select
            case
                when wtid = 410901813 then 410923
                else wfid
            end wfid , sum("MH.TotEgyAt.Wt.F32.OZ[max]"-"MH.TotEgyAt.Wt.F32.OZ[min]") OGC
        from
            public.statisticdata_view_11
        where
            wtid in (410901812, 410922801, 410526801, 410901813,410728850,410546850,411101821,410402801)
            and rectime > to_timestamp(concat(to_char(current_date-2, 'yyyy-mm-dd') , ' 23:50:00'), 'yyyy-MM-dd hh24:mi:ss')
            and rectime <= to_timestamp(concat(to_char(current_date-1, 'yyyy-mm-dd') , ' 23:50:00'), 'yyyy-MM-dd hh24:mi:ss')
        group by
            case
                when wtid = 410901813 then 410923
                else wfid
            end) cc ) cc on
    aa.wfid = cc.wfid

'''
