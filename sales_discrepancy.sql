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
        sales_erp e
    JOIN
        sales_csv c ON e.sales_id = c.sales_id
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
FROM
    sales_comparison;
