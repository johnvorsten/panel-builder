/****** Script for SelectTopNRows command from SSMS  ******/
/*POINTBAS includes all points, but includes the L2SL point type*/
SELECT COUNT(POINTID)
FROM POINTBAS

SELECT *
FROM POINTBAS

/*POINTFUN includes all points, and includes 
duplicate point IDs for the L2SL point type - they are broken into LDO and LDI*/
SELECT COUNT(distinct POINTID) AS [distinct], count(POINTID) as [total]
FROM POINTFUN

select *
from POINTFUN
full JOIN POINTSEN
ON POINTFUN.POINTID = POINTSEN.POINTID
WHERE TYPE = 'LAO' AND
SENSORTYPE != 'CURRENT' AND
NETDEVID = 'TIDWELL.L03.71601' AND 
VIRTUAL = 0

select * 
from POINTFUN
full JOIN POINTSEN
ON POINTFUN.POINTID = POINTSEN.POINTID
WHERE TYPE = 'LDI' AND
NETDEVID = 'TIDWELL.L03.71601' AND 
VIRTUAL = 0

/* duplicate point IDs*/
SELECT *
FROM POINTFUN
WHERE POINTID IN
	(SELECT POINTID
	FROM POINTFUN
	GROUP BY POINTID
	HAVING COUNT(POINTID) >=2)

/*
Filter by point type
Filter by Panel
Filter by sensor function
*/

select 
sum(case when [t1].[TYPE] = 'LAI' AND [t1].[NETDEVID] = 'TIDWELL.L03.71601' AND [t1].[SENSORTYPE] = 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAICurrent],
sum(case when [t1].[TYPE] = 'LAI' AND [t1].[NETDEVID] = 'TIDWELL.L03.71601' AND [t1].[SENSORTYPE] != 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAIStandard],
sum(case when [t1].[TYPE] = 'LAO' AND [t1].[NETDEVID] = 'TIDWELL.L03.71601' AND [t1].[SENSORTYPE] = 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAOCurrent],
sum(case when [t1].[TYPE] = 'LAO' AND [t1].[NETDEVID] = 'TIDWELL.L03.71601' AND [t1].[SENSORTYPE] != 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAOStandard],
sum(case when [t1].[TYPE] = 'LDI' AND [t1].[NETDEVID] = 'TIDWELL.L03.71601' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LDI],
sum(case when [t1].[TYPE] = 'LDO' AND [t1].[NETDEVID] = 'TIDWELL.L03.71601' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LDO],
sum(case when [t1].[TYPE] = 'LPACI' AND [t1].[NETDEVID] = 'TIDWELL.L03.71601' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LPACI]
	FROM (select [POINTFUN].[POINTID], [TYPE], [VIRTUAL], [NETDEVID], [SENSORTYPE]
		from POINTFUN
		full JOIN POINTSEN
		ON POINTFUN.POINTID = POINTSEN.POINTID) AS [t1];

select
sum(case when [t1].[TYPE] = 'LAI' AND [t1].[NETDEVID] = 'TIDWELL.L00.71603' AND [t1].[SENSORTYPE] = 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAICurrent],
sum(case when [t1].[TYPE] = 'LAI' AND [t1].[NETDEVID] = 'TIDWELL.L00.71603' AND [t1].[SENSORTYPE] != 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAIStandard],
sum(case when [t1].[TYPE] = 'LAO' AND [t1].[NETDEVID] = 'TIDWELL.L00.71603' AND [t1].[SENSORTYPE] = 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAOCurrent],
sum(case when [t1].[TYPE] = 'LAO' AND [t1].[NETDEVID] = 'TIDWELL.L00.71603' AND [t1].[SENSORTYPE] != 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAOStandard],
sum(case when [t1].[TYPE] = 'LDI' AND [t1].[NETDEVID] = 'TIDWELL.L00.71603' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LDI],
sum(case when [t1].[TYPE] = 'LDO' AND [t1].[NETDEVID] = 'TIDWELL.L00.71603' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LDO],
sum(case when [t1].[TYPE] = 'LPACI' AND [t1].[NETDEVID] = 'TIDWELL.L00.71603' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LPACI]
	FROM (select [POINTFUN].[POINTID], [TYPE], [VIRTUAL], [NETDEVID], [SENSORTYPE]
		from POINTFUN
		full JOIN POINTSEN
		ON POINTFUN.POINTID = POINTSEN.POINTID) AS [t1];


select
sum(case when [t1].[TYPE] = 'LAI' AND [t1].[NETDEVID] = 'TIDWELL.L04.71602' AND [t1].[SENSORTYPE] = 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAICurrent],
sum(case when [t1].[TYPE] = 'LAI' AND [t1].[NETDEVID] = 'TIDWELL.L04.71602' AND [t1].[SENSORTYPE] != 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAIStandard],
sum(case when [t1].[TYPE] = 'LAO' AND [t1].[NETDEVID] = 'TIDWELL.L04.71602' AND [t1].[SENSORTYPE] = 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAOCurrent],
sum(case when [t1].[TYPE] = 'LAO' AND [t1].[NETDEVID] = 'TIDWELL.L04.71602' AND [t1].[SENSORTYPE] != 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAOStandard],
sum(case when [t1].[TYPE] = 'LDI' AND [t1].[NETDEVID] = 'TIDWELL.L04.71602' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LDI],
sum(case when [t1].[TYPE] = 'LDO' AND [t1].[NETDEVID] = 'TIDWELL.L04.71602' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LDO],
sum(case when [t1].[TYPE] = 'LPACI' AND [t1].[NETDEVID] = 'TIDWELL.L04.71602' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LPACI]
	FROM (select [POINTFUN].[POINTID], [TYPE], [VIRTUAL], [NETDEVID], [SENSORTYPE]
		from POINTFUN
		full JOIN POINTSEN
		ON POINTFUN.POINTID = POINTSEN.POINTID) AS [t1];