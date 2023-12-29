CREATE TABLE sales (
    sales_id SERIAL PRIMARY KEY,
    sales_at TIMESTAMP NOT NULL,
    shipping DECIMAL(10, 2),
    discount DECIMAL(10, 2),
    total_transaction DECIMAL(10, 2)
);

CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    last_price DECIMAL(10, 2)
);

CREATE TABLE sales_item (
    sales_id INT,
    product_id INT,
    qty INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    subtotal AS (qty * price) STORED,
    PRIMARY KEY (sales_id, product_id),
    FOREIGN KEY (sales_id) REFERENCES sales (sales_id),
    FOREIGN KEY (product_id) REFERENCES product (product_id)
);
