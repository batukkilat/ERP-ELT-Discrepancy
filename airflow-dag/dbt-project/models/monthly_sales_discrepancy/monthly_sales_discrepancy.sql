WITH monthly_sales_comparison AS (
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
        sales_erp  AS e
    JOIN
        sales_csv  AS c
    ON 
        e.sales_id = c.sales_id
)
SELECT
    DATE_TRUNC('month', COALESCE(system_datetime::date, spreadsheet_datetime::date)) AS month_bucket,
    SUM(ABS(COALESCE(system_total_transaction, 0) - COALESCE(spreadsheet_total_transaction, 0))) AS total_discrepancy,
    SUM(CASE WHEN system_total_discount <> spreadsheet_total_discount THEN 1 ELSE 0 END) AS inequal_total_discount_discrepancy,
    SUM(CASE WHEN system_total_shipping <> spreadsheet_total_shipping THEN 1 ELSE 0 END) AS inequal_total_shipping_discrepancy,
    SUM(CASE WHEN system_total_transaction <> spreadsheet_total_transaction THEN 1 ELSE 0 END) AS invalid_system_calculation_discrepancy,
    SUM(CASE WHEN system_total_transaction <> spreadsheet_total_transaction THEN 1 ELSE 0 END) AS invalid_spreadsheet_calculation_discrepancy
FROM
    monthly_sales_comparison
GROUP BY
    DATE_TRUNC('month', COALESCE(system_datetime::date, spreadsheet_datetime::date))
