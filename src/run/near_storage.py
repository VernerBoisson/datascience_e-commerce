import pandas as pd
import yaml
import seaborn as sns
import matplotlib.pyplot as plt

with open('../../params/configs/data_path.yaml', 'r') as fp:
    data_path = yaml.load(fp)
seller = pd.read_csv(data_path['olist_sellers_dataset'])
geolocation = pd.read_csv(data_path['olist_geolocation_dataset'])
customers = pd.read_csv(data_path['olist_customers_dataset'])
df= seller

#Cette fonction donne l'entrepôt le plus proche du client
def nearStorage(zip_code,city): #La fonction prends deux arguments, le zip_code qui est le zip code de la commande, et la city qui est la ville où la commande est passé
    compteur = 0 #le compteur qui est utilisé pour atteindre la ligne que l'on souhaite dans le dataframe
    for i in df['seller_zip_code_prefix'] :
        if(i == zip_code):
            return df.iloc[compteur] #si on trouve un zip_code correspondant, alors, on renvoie la ligne de la dataframe correspondante
        else :
            compteur+=1;
    tempo = []
    compteur =0
    for i in df['seller_city']: #Si nous n'avons pas trouvé de zip_code correspondant alors
        if(i == city):
            tempo.append(df.iloc[compteur]['seller_id']) # on prends tout les entrepôts de la ville recherché.
            compteur+=1;
        else:
            compteur+=1;
    if(tempo==[]):return "Aucun entrepôt à proximité" #Si aucune entrepôt n'a été trouvé alors on renvoie ce message
    return tempo #Sinon on renvoie un tableau d'id d'entrepôt. Avec les id d'entrepôt on pourrais, par exemple, envoyer les produit dans l'entrepôt le moins surchargé.
with open('../../params/configs/near_storage.yaml', 'r') as fp:
    params = yaml.load(fp)
print(nearStorage(params['zip_code'], params['city']))
