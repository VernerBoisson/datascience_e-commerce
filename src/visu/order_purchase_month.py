import pandas as pd
import yaml
import seaborn as sns
import matplotlib.pyplot as plt

with open('../../params/configs/data_path.yaml', 'r') as fp:
    data_path = yaml.load(fp)
df_orders = pd.read_csv(data_path['olist_orders_dataset'])
df = df_orders
df['order_purchase_at'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
df['order_purchase_at_ym'] = df['order_purchase_at'].dt.to_period('M')
df.sort_values(by="order_purchase_at_ym", inplace=True)
plt.figure(figsize=(16, 10))
sns.countplot(data=df_orders, x='order_purchase_at_ym', palette="Set3")
plt.ylabel("Nombre de commande effectué")
plt.xlabel("Date")
plt.title("Nombre de commande par mois")
plt.xticks(rotation=45)
plt.savefig('../../params/plot/product_year/order_purchase_month.png')
plt.show()
