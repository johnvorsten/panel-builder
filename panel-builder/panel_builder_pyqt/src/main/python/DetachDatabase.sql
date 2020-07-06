USE [master]
        GO
        ALTER DATABASE [PBJobDB20200110220259] SET SINGLE_USER WITH ROLLBACK IMMEDIATE
        GO
        EXEC master.dbo.sp_detach_db @dbname = N'PBJobDB20200110220259', @skipchecks = 'false'
        GO