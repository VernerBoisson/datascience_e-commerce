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
df['order_approved_at_ymd'] = df['order_approved_at'].dt.to_period('d')
df.sort_values(by="order_approved_at_ymd", inplace=True)


def top_product_by_time_interval(start_date, end_date, number_articles, save_directory='./'):
    df_tmp = df[df.order_approved_at_ymd.between(start_date, end_date)]
    category_count = df_tmp['product_id'].value_counts()[:number_articles]
    category_list = category_count.index.tolist()
    for i in category_list:
        try:
            plt.figure(figsize=(16, 10))
            sns.countplot(data=df_tmp[df_tmp['product_id'] == i], x='order_approved_at_ymd', palette="Set3")
            plt.ylabel("Nombre de commande effectué")
            plt.xlabel("Date")
            plt.xticks(rotation=90)
            plt.title("Nombre de commande par jour pour l'article %s de %s à %s" % (i, start_date, end_date))
            plt.savefig('%s\product_%s_%s_%s.png' % (save_directory, i, start_date[:10], end_date[:10]))
            plt.show()
        except:
            print()
    return None


with open('../../params/configs/top_product_interval.yaml', 'r') as fp:
    params = yaml.load(fp)
top_product_by_time_interval(params['start_date'], params['end_date'], params['top_number'], params['save_directory'])
