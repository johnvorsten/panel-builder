USE [master]
        GO
        ALTER DATABASE [PBJobDB] SET SINGLE_USER WITH ROLLBACK IMMEDIATE
        GO
        EXEC master.dbo.sp_detach_db @dbname = N'PBJobDB', @skipchecks = 'false'
        GO