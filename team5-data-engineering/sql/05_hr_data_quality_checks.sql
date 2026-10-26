USE AdventureWorks2025;
GO

-- 1. Check employee key uniqueness
SELECT
    COUNT(*) AS TotalRows,
    COUNT(DISTINCT BusinessEntityID) AS UniqueEmployeeIDs
FROM HumanResources.Employee;

-- 2. Check missing values in important HR fields
SELECT
    SUM(CASE WHEN OrganizationNode IS NULL THEN 1 ELSE 0 END)
        AS MissingOrganizationNode,
    SUM(CASE WHEN OrganizationLevel IS NULL THEN 1 ELSE 0 END)
        AS MissingOrganizationLevel
FROM HumanResources.Employee;

-- 3. Check current department assignments
SELECT
    COUNT(*) AS TotalHistoryRows,
    SUM(CASE WHEN EndDate IS NULL THEN 1 ELSE 0 END)
        AS RowsWithNoEndDate
FROM HumanResources.EmployeeDepartmentHistory;

-- 4. Check candidate records without an employee link
SELECT
    COUNT(*) AS TotalCandidates,
    SUM(CASE WHEN BusinessEntityID IS NULL THEN 1 ELSE 0 END)
        AS CandidatesWithoutEmployee
FROM HumanResources.JobCandidate;

-- 5. Check for non-positive pay rates
SELECT COUNT(*) AS NonPositivePayRates
FROM HumanResources.EmployeePayHistory
WHERE Rate <= 0;