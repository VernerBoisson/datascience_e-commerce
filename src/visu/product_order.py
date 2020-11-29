import pandas as pd
import yaml
import seaborn as sns
import matplotlib.pyplot as plt

with open('../../params/configs/data_path.yaml', 'r') as fp:
    data_path = yaml.load(fp)
df_orders = pd.read_csv(data_path['olist_orders_dataset'])
df_customers = pd.read_csv(data_path['olist_customers_dataset'])
df_oder_item = pd.read_csv(data_path['olist_order_items_dataset'])

df = pd.merge(df_orders, df_customers, on='customer_id')
df = pd.merge(df, df_oder_item, on='order_id')

df_product_id = pd.DataFrame(df.product_id.value_counts())
df_product_id['unique'] = pd.DataFrame(df.product_id.value_counts() > 1)
df_product_id['str_unique'] = df_product_id['unique'].replace(
    {False:"un article", True:"plusieurs articles"})

plt.figure(figsize=(10,10))
sns.countplot(data=df_product_id, x='str_unique', palette="Set3")
plt.ylabel("Nombre de commandes")
plt.xlabel('')
plt.title("Nombre de commandes composé de plusieurs articles")
plt.savefig('../../params/plot/suggestion/product_by_order.png')
plt.show()