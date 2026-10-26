
-- -- 1. Invalid department references
-- SELECT COUNT(*) AS InvalidDepartmentReferences
-- FROM HumanResources.EmployeeDepartmentHistory h
-- LEFT JOIN HumanResources.Department d
--     ON h.DepartmentID = d.DepartmentID
-- WHERE d.DepartmentID IS NULL;

-- -- 2. Invalid shift references
-- SELECT COUNT(*) AS InvalidShiftReferences
-- FROM HumanResources.EmployeeDepartmentHistory h
-- LEFT JOIN HumanResources.Shift s
--     ON h.ShiftID = s.ShiftID
-- WHERE s.ShiftID IS NULL;

-- -- 3. Duplicate department IDs
-- SELECT DepartmentID, COUNT(*) AS RecordCount
-- FROM HumanResources.Department
-- GROUP BY DepartmentID
-- HAVING COUNT(*) > 1;

-- -- 4. Duplicate shift IDs
-- SELECT ShiftID, COUNT(*) AS RecordCount
-- FROM HumanResources.Shift
-- GROUP BY ShiftID
-- HAVING COUNT(*) > 1;

-- Check duplicate department records
-- SELECT
--     Name,
--     GroupName,
--     COUNT(*) AS RecordCount
-- FROM HumanResources.Department
-- GROUP BY Name, GroupName
-- HAVING COUNT(*) > 1;

-- -- Check duplicate shift records
-- SELECT
--     Name,
--     StartTime,
--     EndTime,
--     COUNT(*) AS RecordCount
-- FROM HumanResources.Shift
-- GROUP BY Name, StartTime, EndTime
-- HAVING COUNT(*) > 1;

-- SELECT
--     BusinessEntityID,
--     DepartmentID,
--     StartDate,
--     EndDate
-- FROM HumanResources.EmployeeDepartmentHistory
-- WHERE EndDate < StartDate;
-- SELECT
--     a.BusinessEntityID,
--     a.DepartmentID,
--     a.StartDate AS FirstStartDate,
--     a.EndDate AS FirstEndDate,
--     b.StartDate AS SecondStartDate,
--     b.EndDate AS SecondEndDate
-- FROM HumanResources.EmployeeDepartmentHistory a
-- JOIN HumanResources.EmployeeDepartmentHistory b
--     ON a.BusinessEntityID = b.BusinessEntityID
--    AND a.DepartmentID = b.DepartmentID
--    AND a.StartDate < b.StartDate
-- WHERE
--     a.EndDate IS NULL
--     OR a.EndDate >= b.StartDate;




