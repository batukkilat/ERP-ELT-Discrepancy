import pandas as pd

df = pd.read_csv('products.csv')

df.head()

df.columns = ['sales_id', 'sales_at', 'shipping', 'discount', 'total_transaction']

df.to_csv('products1.csv')