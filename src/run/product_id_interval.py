import pandas as pd
import yaml
import seaborn as sns
import matplotlib.pyplot as plt

with open('../../params/configs/data_path.yaml', 'r') as fp:
    data_path = yaml.load(fp)
df_oder_item = pd.read_csv(data_path['olist_order_items_dataset'])
df_product = pd.read_csv(data_path['olist_products_dataset'])
df_orders = pd.read_csv(data_path['olist_orders_dataset'])
translation = pd.read_csv(data_path['product_category_name_translation'])
df = pd.merge(df_product, df_oder_item, on='product_id')
df = pd.merge(df, df_orders, on='order_id')
df['order_approved_at'] = pd.to_datetime(df['order_approved_at'], errors='coerce')
df['order_approved_at_ym'] = df['order_approved_at'].dt.to_period('M')
df['order_approved_at_ymd'] = df['order_approved_at'].dt.to_period('d')
df.sort_values(by="order_approved_at_ymd", inplace=True)


def plot_product_id_with_tiem_interval(product_id, start_date, end_date, save_directory):
    df_tmp = df[df.order_approved_at_ymd.between(start_date, end_date)]
    df_tmp = df_tmp[df_tmp['product_id']==product_id]
    try:
        plt.figure(figsize=(16,10))
        sns.countplot(data=df_tmp, x='order_approved_at_ym', palette="Set3")
        plt.ylabel("Nombre de commande effectué")
        plt.xlabel("Date")
        plt.xticks(rotation=90)
        plt.title("Nombre de commande par mois pour l'article %s de %s à %s" % (product_id, start_date, end_date))
        plt.savefig('%s\product_mounth_%s_%s_%s.png' % (save_directory, product_id, start_date[:10], end_date[:10]))
        plt.show()
        plt.figure(figsize=(16,10))
        sns.countplot(data=df_tmp, x='order_approved_at_ymd', palette="Set3")
        plt.ylabel("Nombre de commande effectué")
        plt.xlabel("Date")
        plt.xticks(rotation=90)
        plt.title("Nombre de commande par jour pour l'article %s de %s à %s" % (product_id, start_date, end_date))
        plt.savefig('%s\product_days_%s_%s_%s.png' % (save_directory, product_id, start_date[:10], end_date[:10]))
        plt.show()
    except:
        print()
    return None

with open('../../params/configs/product_id_interval.yaml', 'r') as fp:
    params = yaml.load(fp)
plot_product_id_with_tiem_interval(params['product_id'], params['start_date'], params['end_date'], params['save_directory'])