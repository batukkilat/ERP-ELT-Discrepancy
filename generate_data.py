from typing import List
import datetime
import random

class Product():
    def __init__(self, id: int, name: str, last_price: float):
        self.id = id
        self.name = name
        self.last_price = last_price
    
    def to_sql(self) -> str:
        return ' '.join([
            'INSERT INTO product (product_id, product_name, last_price)',
            f"VALUES ({self.id}, '{self.name}', {self.last_price});"
        ])

    def to_csv(self) -> str:
        return f"{self.id},\"{self.name}\",{self.last_price}"


class ProductDetail():
    def __init__(self, product: Product, qty: int):
        self.product = product
        self.qty = qty
    

class Transaction:
    def __init__(
        self, 
        id: int, 
        sales_at: datetime.datetime, 
        shipping: float, 
        discount: float, 
        sales_item: List[ProductDetail],
        error_rate: float = 0.1
    ):
        self.id = id
        self.sales_at = sales_at
        self.shipping = shipping
        self.discount = discount
        self.sales_item = sales_item
        self.total_transaction = sum(p.product.last_price * p.qty for p in sales_item) + self.shipping - self.discount
        self.error_rate = error_rate

    def to_sql_sales(self) -> str:
        error_applied = False
        shipping = self.shipping
        if not error_applied and random.random() > self.error_rate:
            shipping += random.randint(-1000, 1000)
            error_applied = True
        discount = self.discount
        if not error_applied and random.random() > self.error_rate:
            discount += random.randint(-1000, 1000)
            error_applied = True
        total_transaction = self.total_transaction
        if not error_applied and random.random() > self.error_rate:
            total_transaction += random.randint(-1000, 1000)
            error_applied = True
        return ' '.join([
            'INSERT INTO sales (sales_id, sales_at, shipping, discount, total_transaction)',
            f"VALUES ({self.id}, '{self.sales_at.strftime('%Y-%m-%d %H:%M:%S')}', {shipping}, {discount}, {total_transaction});"
        ])

    def to_csv_sales(self) -> str:
        shipping = self.shipping
        discount = self.discount
        total_transaction = self.total_transaction
        return f"{self.id},\"{self.sales_at.strftime('%Y-%m-%d %H:%M:%S')}\",{shipping},{discount},{total_transaction}"

    def to_sql_sales_item(self) -> str:
        error_applied = False
        sql_statements = []
        for item in self.sales_item:
            if not error_applied and random.random() > self.error_rate:
                error_applied = True
                continue
            sql_statements.append(' '.join([
                'INSERT INTO sales_item (sales_id, product_id, qty, price, subtotal)',
                f"VALUES ({self.id}, {item.product.id}, {item.qty}, {item.product.last_price}, {item.qty * item.product.last_price});"
            ]))
        return '\n'.join(sql_statements)

    def to_csv_sales_item(self) -> str:
        csv_lines = []
        for item in self.sales_item:
            csv_lines.append(f"{self.id},{item.product.id},{item.qty},{item.product.last_price},{item.qty * item.product.last_price}")
        return '\n'.join(csv_lines)


def create_random_date_time(
    start_date = datetime.datetime(2023, 1, 1),
    end_date = datetime.datetime(2023, 10, 31)
):
    delta = end_date - start_date
    random_number_of_days = random.randint(0, delta.days)
    random_number_of_seconds = random.randint(0, 24 * 60 * 60)
    random_date_time = start_date + datetime.timedelta(days=random_number_of_days, seconds=random_number_of_seconds)
    return random_date_time


if __name__ == '__main__':
    products = [
        Product(id=1, name='dompet', last_price=50000),
        Product(id=2, name='baju', last_price=100000),
        Product(id=3, name='celana', last_price=200000),
        Product(id=4, name='pensil', last_price=5000),
    ]
    product_count = len(products)

    transactions = []
    for id in range(1, 1000):
        sales_at = create_random_date_time(
            start_date = datetime.datetime(2023, 1, 1),
            end_date = datetime.datetime(2023, 10, 1),
        )
        # error rate is decreasing over time
        error_rate = 0
        if sales_at.month < 10:
            error_rate = (10 - sales_at.month) / 10.0
        item_count = random.randint(0, product_count - 1)
        sales_item = []
        for item_index in range(item_count):
            sales_item.append(
                ProductDetail(
                    product=products[item_index],
                    qty=random.randint(1, 5)
                )
            )
        transactions.append(
            Transaction(
                id=id,
                sales_at=sales_at,
                shipping=random.randint(0, 5) * 1000,
                discount=random.randint(0, 10) * 10000,
                sales_item=sales_item,
                error_rate=error_rate
            )
        )


    product_csv = '\n'.join([
        product.to_csv() for product in products
    ])
    with open('products.csv', 'w') as f:
        f.write(product_csv)

    product_sql = '\n'.join([
        product.to_sql() for product in products
    ])
    with open('products.sql', 'w') as f:
        f.write(product_sql)

    sales_csv = '\n'.join([
        transaction.to_csv_sales() for transaction in transactions
    ])
    with open('sales.csv', 'w') as f:
        f.write(sales_csv)

    sales_sql = '\n'.join([
        transaction.to_sql_sales() for transaction in transactions
    ])
    with open('sales.sql', 'w') as f:
        f.write(sales_sql)

    sales_item_csv = '\n'.join([
        transaction.to_csv_sales_item() for transaction in transactions
    ])
    with open('sales_item.csv', 'w') as f:
        f.write(sales_item_csv)

    sales_item_sql = '\n'.join([
        transaction.to_sql_sales_item() for transaction in transactions
    ])
    with open('sales_item.sql', 'w') as f:
        f.write(sales_item_sql)