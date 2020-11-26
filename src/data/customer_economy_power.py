import pandas as pd
import yaml

with open('../../params/configs/data_path.yaml', 'r') as fp:
    data_path = yaml.load(fp)
df_oder_item = pd.read_csv(data_path['olist_order_items_dataset'])
df_product = pd.read_csv(data_path['olist_products_dataset'])
df_orders = pd.read_csv(data_path['olist_orders_dataset'])
df_customers = pd.read_csv(data_path['olist_customers_dataset'])

df = pd.merge(df_orders, df_customers, on='customer_id')
df = pd.merge(df, df_oder_item, on='order_id')
df = pd.merge(df, df_product, on='product_id')
df_agg = df.groupby(['customer_unique_id']).agg({'customer_unique_id': "count", 'price': "sum"})

# Score arbitrairement choisit qui met en avant la somme total dépensée ainsi que le nombre de commande
df_agg['eco_score'] = df_agg.price / 100 * df_agg.customer_unique_id * 0.25
df_agg = df_agg.sort_values(['eco_score'], ascending=False)

#Les 5% de consommateur ayant le plus de pouvoir économique
df_top = pd.DataFrame(df_agg['eco_score'][:int(df_agg.shape[0] * 5 / 100)])
print(df_top.head(10).to_markdown())


