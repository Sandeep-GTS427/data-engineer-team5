
USE AdventureWorks2025;
GO

SELECT
    BusinessEntityID,
    JobTitle,
    OrganizationNode,
    OrganizationLevel
FROM HumanResources.Employee
WHERE OrganizationNode IS NULL
   OR OrganizationLevel IS NULL;
