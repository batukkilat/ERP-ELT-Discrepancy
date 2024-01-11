WITH sales_detail_comparison AS (
    SELECT
        e.sales_id AS system_order_id,
        e.product_id AS system_item_id,
        e.qty AS system_qty,
        e.price AS system_price,
        e.subtotal AS system_subtotal,
        c.sales_id AS spreadsheet_order_id,
        c.product_id AS spreadsheet_item_id,
        c.qty AS spreadsheet_qty,
        c.price AS spreadsheet_price,
        c.subtotal AS spreadsheet_subtotal
    FROM
        {{ source('store', 'sales_item_erp') }} AS e
    JOIN
        {{ source('store', 'sales_item_csv') }} AS c 
    ON 
        e.sales_id = c.sales_id
)

SELECT
    system_order_id,
    system_item_id,
    system_qty,
    system_price,
    system_subtotal,
    spreadsheet_order_id,
    spreadsheet_item_id,
    spreadsheet_qty,
    spreadsheet_price,
    spreadsheet_subtotal,
    ABS(system_subtotal - spreadsheet_subtotal) AS discrepancy
FROM
    sales_detail_comparison;
