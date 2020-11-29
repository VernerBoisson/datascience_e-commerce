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
translation = pd.read_csv(data_path['product_category_name_translation'])

df = pd.merge(df_orders, df_customers, on='customer_id')
df = pd.merge(df, df_oder_item, on='order_id')
df = pd.merge(df, df_product, on='product_id')
df = pd.merge(df, translation, on='product_category_name')

category_count = df['product_category_name_english'].value_counts()
category_list = category_count[category_count > 8000].index.tolist()
df = df[df['product_category_name_english'].isin(category_list)]

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot()
sns.stripplot(data=df, y='customer_id', x='product_category_name_english', palette="Set2")
plt.xlabel("Catégorie d'articles")
plt.ylabel("Consommateurs")
ax.set_yticks([])
plt.title("Répartition des consommateurs selon les catégories d'articles")
plt.savefig('../../params/plot/suggestion/customer_category_2.png')
plt.show()
