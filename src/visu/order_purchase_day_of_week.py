import pandas as pd
import yaml
import seaborn as sns
import matplotlib.pyplot as plt

with open('../../params/configs/data_path.yaml', 'r') as fp:
    data_path = yaml.load(fp)
df_orders = pd.read_csv(data_path['olist_orders_dataset'])
df = df_orders

df['order_purchase_at'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
df['order_purchase_at_ymd'] = df['order_purchase_at'].dt.to_period('d')
df['order_purchase_at_day'] = df['order_purchase_at'].dt.dayofweek
df.sort_values(by="order_purchase_at_day", inplace=True)
df['order_purchase_at_day'] = df['order_purchase_at_day'].replace(
    {0:"Lun", 1:"Mar", 2:"Mer", 3:"Jeu", 4:"Ven", 5:"Sam", 6:"Dim"})
plt.figure(figsize=(10,10))
sns.countplot(data=df, x='order_purchase_at_day', palette="Set3")
plt.ylabel("Nombre de commande effectué")
plt.xlabel("Jour")
plt.title("Nombre de commande par jour de la semaine")
plt.savefig('../../params/plot/product_year/order_purchase_day_of_week.png')
plt.show()