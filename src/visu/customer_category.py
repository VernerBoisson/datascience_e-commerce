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

category_count = df['product_category_name'].value_counts()[:30]
category_list = category_count.index.tolist()

df_customer_unique = df.customer_unique_id.value_counts()[:1000]
list_consumer = df_customer_unique.index

df = df[df.customer_unique_id.isin(list_consumer)]
df = df[df.product_category_name.isin(category_list)]

fig = plt.figure(figsize=(20, 20))
ax = fig.add_subplot()
sns.scatterplot(data=df, x='customer_unique_id', y='product_category_name')
plt.xticks(rotation=90)
plt.ylabel("Cartégorie d'article")
plt.xlabel('Consommateur')
ax.set_yticks([])
ax.set_xticks([])
plt.title("Répartition des articles par rapport aux consommateurs")
plt.savefig('../../params/plot/suggestion/customer_category.png')
plt.show()
