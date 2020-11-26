import pandas as pd
import yaml
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

with open('../../params/configs/data_path.yaml', 'r') as fp:
    data_path = yaml.load(fp)
df_orders = pd.read_csv(data_path['olist_orders_dataset'])
df = df_orders
df['order_purchase_at'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
df['order_purchase_at_ymd'] = df['order_purchase_at'].dt.to_period('d')
df.sort_values(by="order_purchase_at_ymd", inplace=True)
df = df[df.order_purchase_at_ymd.between('2017-11-01', '2017-12-10')]

fig = plt.figure(figsize=(16, 10))
ax = fig.add_subplot()
sns.countplot(data=df, x='order_purchase_at_ymd', color='grey')
plt.ylabel("Nombre de commande effectué")
plt.xlabel("Date")
ax.patches[23].set_facecolor('darkred')
name_to_color = {
    'Black Friday': 'darkred',
}
patches = [matplotlib.patches.Patch(color=v, label=k) for k, v in name_to_color.items()]
matplotlib.pyplot.legend(handles=patches)
plt.title("Nombre de commande par jour pour le mois de novembre 2017")
plt.xticks(rotation=70)
plt.savefig('../../params/plot/product_year/order_purchase_november.png')
plt.show()
