import pandas as pd
import yaml
import seaborn as sns
import matplotlib.pyplot as plt

with open('../../params/configs/data_path.yaml', 'r') as fp:
    data_path = yaml.load(fp)
df_orders = pd.read_csv(data_path['olist_orders_dataset'])
df_customers = pd.read_csv(data_path['olist_customers_dataset'])
df_oder_item = pd.read_csv(data_path['olist_order_items_dataset'])
df_product = pd.read_csv(data_path['olist_products_dataset'])

df = pd.merge(df_orders, df_customers, on='customer_id')
df = pd.merge(df, df_oder_item, on='order_id')
df = pd.merge(df, df_product, on='product_id')

df_customer_unique = df.customer_unique_id.value_counts()[:1000]
list_consumer = df_customer_unique.index

product_count = df_oder_item['product_id'].value_counts()[:100000]
product_list = product_count.index.tolist()

df = df[df.customer_unique_id.isin(list_consumer)]
df = df[df.product_id.isin(product_list)]

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot()
sns.scatterplot(data=df, x='customer_unique_id', y='product_id')
plt.xticks(rotation=90)
plt.ylabel('Article')
plt.xlabel('Consommateur')
ax.set_yticks([])
ax.set_xticks([])
plt.title("Répartition des articles par rapport aux consommateurs")
plt.savefig('../../params/plot/suggestion/customer_product.png')
plt.show()