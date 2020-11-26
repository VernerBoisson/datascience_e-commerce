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

df_customer_unique = pd.DataFrame(df.customer_unique_id.value_counts())
df_customer_unique['unique'] = pd.DataFrame(df.customer_unique_id.value_counts() > 1)
df_customer_unique['str_unique'] = df_customer_unique['unique'].replace(
    {False:"une commande", True:"plusieurs commandes"})

plt.figure(figsize=(10,10))
sns.countplot(data=df_customer_unique, x='str_unique', palette="Set3")
plt.ylabel("Nombre de consommateur")
plt.xlabel('')
plt.title("Nombre de consommateur récurrent")
plt.savefig('../../params/plot/suggestion/order_by_costumer.png')
plt.show()