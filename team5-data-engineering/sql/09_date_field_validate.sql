
-- -- Check birth dates after hire dates
-- SELECT
--     BusinessEntityID,
--     BirthDate,
--     HireDate,
--     JobTitle
-- FROM HumanResources.Employee
-- WHERE BirthDate > HireDate;

-- -- Check future birth dates
-- SELECT
--     BusinessEntityID,
--     BirthDate,
--     JobTitle
-- FROM HumanResources.Employee
-- WHERE BirthDate > CAST(GETDATE() AS date);

-- -- Check future hire dates
-- SELECT
--     BusinessEntityID,
--     HireDate,
--     JobTitle
-- FROM HumanResources.Employee
-- WHERE HireDate > CAST(GETDATE() AS date);
SELECT
    SUM(CASE WHEN BirthDate > HireDate
        THEN 1 ELSE 0 END) AS BirthAfterHire,
    SUM(CASE WHEN BirthDate > CAST(GETDATE() AS date)
        THEN 1 ELSE 0 END) AS FutureBirthDates,
    SUM(CASE WHEN HireDate > CAST(GETDATE() AS date)
        THEN 1 ELSE 0 END) AS FutureHireDates
FROM HumanResources.Employee;
