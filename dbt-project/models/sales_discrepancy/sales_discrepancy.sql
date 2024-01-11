WITH sales_comparison AS (
    SELECT
        e.sales_id AS system_order_id,
        e.sales_at AS system_datetime,
        e.discount AS system_total_discount,
        e.shipping AS system_total_shipping,
        e.total_transaction AS system_total_transaction,
        c.sales_id AS spreadsheet_order_id,
        c.sales_at AS spreadsheet_datetime,
        c.discount AS spreadsheet_total_discount,
        c.shipping AS spreadsheet_total_shipping,
        c.total_transaction AS spreadsheet_total_transaction
    FROM
        {{ source('store', 'sales_erp') }} AS e
    JOIN
        {{ source('store', 'sales_csv') }} AS c
    ON 
        e.sales_id = c.sales_id
)

SELECT
    system_order_id,
    system_datetime,
    system_total_discount,
    system_total_shipping,
    system_total_transaction,
    spreadsheet_order_id,
    spreadsheet_datetime,
    spreadsheet_total_discount,
    spreadsheet_total_shipping,
    spreadsheet_total_transaction,
    ABS(system_total_transaction - spreadsheet_total_transaction) AS discrepancy
    CASE WHEN system_total_discount <> spreadsheet_total_discount THEN 1 ELSE 0 END AS is_inequal_total_discount,
    CASE WHEN system_total_shipping <> spreadsheet_total_shipping THEN 1 ELSE 0 END AS is_inequal_total_shipping,
    CASE WHEN system_total_transaction <> spreadsheet_total_transaction THEN 1 ELSE 0 END AS is_invalid_system_calculation,
    CASE WHEN system_total_transaction <> spreadsheet_total_transaction THEN 1 ELSE 0 END AS is_invalid_spreadsheet_calculation,
    CASE WHEN system_order_id IS NULL THEN 1 ELSE 0 END AS is_missing_system_item,
    CASE WHEN spreadsheet_order_id IS NULL THEN 1 ELSE 0 END AS is_missing_spreadsheet_item
FROM
    sales_comparison;
