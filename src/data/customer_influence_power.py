import pandas as pd
import yaml

with open('../../params/configs/data_path.yaml', 'r') as fp:
    data_path = yaml.load(fp)
df_orders = pd.read_csv(data_path['olist_orders_dataset'])
df_customers = pd.read_csv(data_path['olist_customers_dataset'])
df_reviews = pd.read_csv(data_path['olist_order_reviews_dataset'])

df = pd.merge(df_orders, df_customers, on='customer_id')
df = pd.merge(df, df_reviews, on='order_id')
df = df.dropna(subset=['review_score'])
df_agg = df.groupby(['customer_unique_id']).agg({'customer_unique_id'    : "count",
                                                 'review_score'          : "mean",
                                                 'review_comment_message': "count",
                                                 'review_comment_title'  : "count",
                                                 })

# Score arbitrairement choisit qui met en le nombre de consommateur ayant mit une note,
# la moyenne de ces score ainsi que le nombre de message et de titre de commentaire
df_agg['inf_score'] = (df_agg.customer_unique_id * 2 *
                       df_agg.review_score +
                       df_agg.review_comment_message * 0.25 +
                       df_agg.review_comment_message * 0.25) / 4
df_agg = df_agg.sort_values(['inf_score'], ascending=False)

#Les 5% de consommateur ayant le plus de pouvoir d'influence
df_top = pd.DataFrame(df_agg['inf_score'][:int(df_agg.shape[0]*5/100)])

#Les 5% de consommateur ayant le moins de pouvoir d'influence
df_bot = pd.DataFrame(df_agg['inf_score'][-int(df_agg.shape[0]*5/100):])

print(df_top.to_markdown())
print(df_bot.to_markdown())

