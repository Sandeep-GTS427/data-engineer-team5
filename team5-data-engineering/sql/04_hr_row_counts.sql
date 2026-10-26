USE AdventureWorks2025;
GO

SELECT 'Department' AS TableName, COUNT_BIG(*) AS 'RowCount'
FROM HumanResources.Department

UNION ALL

SELECT 'Employee', COUNT_BIG(*)
FROM HumanResources.Employee

UNION ALL

SELECT 'EmployeeDepartmentHistory', COUNT_BIG(*)
FROM HumanResources.EmployeeDepartmentHistory

UNION ALL

SELECT 'EmployeePayHistory', COUNT_BIG(*)
FROM HumanResources.EmployeePayHistory

UNION ALL

SELECT 'JobCandidate', COUNT_BIG(*)
FROM HumanResources.JobCandidate

UNION ALL

SELECT 'Shift', COUNT_BIG(*)
FROM HumanResources.Shift;