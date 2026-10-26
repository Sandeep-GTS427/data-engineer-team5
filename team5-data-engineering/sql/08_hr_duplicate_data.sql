
-- 1. Check for duplicate complete employee records
SELECT
    BusinessEntityID,
    COUNT(*) AS RecordCount
FROM HumanResources.Employee
GROUP BY BusinessEntityID
HAVING COUNT(*) > 1;

-- 2. Check required employee fields for NULL values
SELECT
    SUM(CASE WHEN NationalIDNumber IS NULL THEN 1 ELSE 0 END)
        AS MissingNationalID,
    SUM(CASE WHEN LoginID IS NULL THEN 1 ELSE 0 END)
        AS MissingLoginID,
    SUM(CASE WHEN JobTitle IS NULL THEN 1 ELSE 0 END)
        AS MissingJobTitle,
    SUM(CASE WHEN BirthDate IS NULL THEN 1 ELSE 0 END)
        AS MissingBirthDate,
    SUM(CASE WHEN HireDate IS NULL THEN 1 ELSE 0 END)
        AS MissingHireDate
FROM HumanResources.Employee;
