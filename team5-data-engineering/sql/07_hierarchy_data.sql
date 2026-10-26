
-- SELECT
--     BusinessEntityID,
--     JobTitle,
--     OrganizationNode.ToString() AS OrganizationPath,
--     OrganizationLevel
-- FROM HumanResources.Employee
-- ORDER BY OrganizationLevel, BusinessEntityID;
SELECT
    OrganizationLevel,
    COUNT(*) AS EmployeeCount,
    SUM(
        CASE WHEN OrganizationNode IS NULL
             THEN 1 ELSE 0 END
    ) AS MissingOrganizationNode,
    SUM(
        CASE WHEN OrganizationNode IS NOT NULL
             THEN 1 ELSE 0 END
    ) AS PresentOrganizationNode
FROM HumanResources.Employee
GROUP BY OrganizationLevel
ORDER BY OrganizationLevel;
