USE AdventureWorks2025;
GO

SELECT
    fk.name AS ForeignKeyName,
    OBJECT_SCHEMA_NAME(fk.parent_object_id) AS ChildSchema,
    OBJECT_NAME(fk.parent_object_id) AS ChildTable,
    COL_NAME(
        fkc.parent_object_id,
        fkc.parent_column_id
    ) AS ChildColumn,
    OBJECT_SCHEMA_NAME(fk.referenced_object_id) AS ParentSchema,
    OBJECT_NAME(fk.referenced_object_id) AS ParentTable,
    COL_NAME(
        fkc.referenced_object_id,
        fkc.referenced_column_id
    ) AS ParentColumn
FROM sys.foreign_keys AS fk
INNER JOIN sys.foreign_key_columns AS fkc
    ON fk.object_id = fkc.constraint_object_id
WHERE OBJECT_SCHEMA_NAME(fk.parent_object_id) = 'HumanResources'
ORDER BY ChildTable, ForeignKeyName;