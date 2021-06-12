/****** Script for SelectTopNRows command from SSMS  ******/
/*POINTBAS includes all points, but includes the L2SL point type*/
DECLARE @controller NVARCHAR(30)
SET @controller = 'PXCM14_7014'

/* Point count showing L2SL as single points */
USE JobDB
SELECT COUNT(POINTID) as [modified_total]
FROM POINTBAS

/*POINTFUN includes all points, and includes 
duplicate point IDs for the L2SL point type - they are broken into LDO and LDI*/
SELECT COUNT(distinct POINTID) AS [distinct], count(POINTID) as [total]
FROM POINTFUN

/* Duplicate point IDs*/
SELECT POINTID as [duplicate_POINTID]
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
LAICurrent - Logical Analog Input with a 'current' input configuration
LAIStandard - Logical Analog Input with a configuration other than 'current'
LAOCurrent - Logical Analog Output with 'curent' configuration
LAOStandard - Logical Analog Output with configuration other than 'current'
LDI - Logical Digital Input (Include L2SL)
LDO - Logical Digital Ooutput (Includes L2SL)
LPACI - Logical Pulsed Accumulator
*/
select 
sum(case when [t1].[TYPE] = 'LAI' AND [t1].[NETDEVID] = @controller AND [t1].[SENSORTYPE] = 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAICurrent],
sum(case when [t1].[TYPE] = 'LAI' AND [t1].[NETDEVID] = @controller AND [t1].[SENSORTYPE] != 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAIStandard],
sum(case when [t1].[TYPE] = 'LAO' AND [t1].[NETDEVID] = @controller AND [t1].[SENSORTYPE] = 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAOCurrent],
sum(case when [t1].[TYPE] = 'LAO' AND [t1].[NETDEVID] = @controller AND [t1].[SENSORTYPE] != 'CURRENT' AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LAOStandard],
sum(case when [t1].[TYPE] = 'LDI' AND [t1].[NETDEVID] = @controller AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LDI],
sum(case when [t1].[TYPE] = 'LDO' AND [t1].[NETDEVID] = @controller AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LDO],
sum(case when [t1].[TYPE] = 'LPACI' AND [t1].[NETDEVID] = @controller AND [t1].[VIRTUAL] = 0 then 1 else 0 end) AS [LPACI]
	FROM (select [POINTFUN].[POINTID], [TYPE], [VIRTUAL], [NETDEVID], [SENSORTYPE]
		from POINTFUN
		full JOIN POINTSEN
		ON POINTFUN.POINTID = POINTSEN.POINTID) AS [t1];


/*Count a specific point type from a specific controller*/
/*
SELECT count([t1].[POINTID]) as TOTAL_COUNT
FROM (select [POINTFUN].[POINTID], [TYPE], [VIRTUAL], [NETDEVID], [SENSORTYPE]
	from POINTFUN
	full JOIN POINTSEN ON POINTFUN.POINTID = POINTSEN.POINTID) AS [t1]
WHERE [t1].[TYPE] = 'LAI'
AND [t1].[NETDEVID] = 'TEMPLATE_PXC' 
AND [t1].[SENSORTYPE] = 'CURRENT' 
AND [t1].[VIRTUAL] = 0
*/