USE [master]
        GO
        ALTER DATABASE [PBJobDB_test] SET SINGLE_USER WITH ROLLBACK IMMEDIATE
        GO
        EXEC master.dbo.sp_detach_db @dbname = N'PBJobDB_test', @skipchecks = 'false'
        GO