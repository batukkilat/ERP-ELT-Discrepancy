WITH sales_detail_comparison AS (
    SELECT
        e.sales_id AS system_order_id,
        e.product_id AS system_item_id,
        p.product_name AS system_product_name,
        e.qty AS system_qty,
        e.price AS system_price,
        e.subtotal AS system_subtotal,
        c.sales_id AS spreadsheet_order_id,
        c.product_id AS spreadsheet_item_id,
        p.product_name AS spreadsheet_product_name,
        c.qty AS spreadsheet_qty,
        c.price AS spreadsheet_price,
        c.subtotal AS spreadsheet_subtotal
    FROM
        sales_item_erp e
    JOIN
        sales_erp c ON e.sales_id = c.sales_id
    JOIN
        products_erp p ON e.product_id = p.product_id
)

SELECT
    system_order_id,
    system_item_id,
    system_product_name,
    system_qty,
    system_price,
    system_subtotal,
    spreadsheet_order_id,
    spreadsheet_item_id,
    spreadsheet_product_name,
    spreadsheet_qty,
    spreadsheet_price,
    spreadsheet_subtotal,
    ABS(system_subtotal - spreadsheet_subtotal) AS discrepancy
FROM
    sales_item_comparison sic;
