
-- 1. Department history referencing missing employees
SELECT COUNT(*) AS InvalidDepartmentEmployeeReferences
FROM HumanResources.EmployeeDepartmentHistory h
LEFT JOIN HumanResources.Employee e
    ON h.BusinessEntityID = e.BusinessEntityID
WHERE e.BusinessEntityID IS NULL;

-- 2. Pay history referencing missing employees
SELECT COUNT(*) AS InvalidPayEmployeeReferences
FROM HumanResources.EmployeePayHistory p
LEFT JOIN HumanResources.Employee e
    ON p.BusinessEntityID = e.BusinessEntityID
WHERE e.BusinessEntityID IS NULL;

-- 3. Job candidates referencing missing employees
SELECT COUNT(*) AS InvalidCandidateEmployeeReferences
FROM HumanResources.JobCandidate j
LEFT JOIN HumanResources.Employee e
    ON j.BusinessEntityID = e.BusinessEntityID
WHERE j.BusinessEntityID IS NOT NULL
  AND e.BusinessEntityID IS NULL;
