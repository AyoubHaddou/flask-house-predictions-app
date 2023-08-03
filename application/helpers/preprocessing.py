import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split  
import warnings
warnings.filterwarnings("ignore")


def neighbors_and_conditions_dict(df):
    neighbors_dict = {}
    for idx, value in enumerate(list(df.groupby('Neighborhood').mean()['SalePrice'].sort_values(ascending=True).index)):
        neighbors_dict[value] = idx 
    return neighbors_dict


def data_augmentation(df, dico_neigbhors ):
    
    dict_subclass = {"1-STORY 1946 & NEWER ALL STYLES": 20,
                                 "1-STORY 1945 & OLDER": 30,
                                 "1-STORY W/FINISHED ATTIC ALL AGES": 40,
                                 "1-1/2 STORY - UNFINISHED ALL AGES": 45,
                                 "1-1/2 STORY FINISHED ALL AGES": 50,
                                 "2-STORY 1946 & NEWER": 60,
                                 "2-STORY 1945 & OLDER": 70,
                                 "2-1/2 STORY ALL AGES": 75,
                                 "SPLIT OR MULTI-LEVEL": 80,
                                 "SPLIT FOYER": 85,
                                 "DUPLEX - ALL STYLES AND AGES": 90,
                                 "1-STORY PUD (Planned Unit Development) - 1946 & NEWER": 120,
                                 "1-1/2 STORY PUD - ALL AGES": 150,
                                 "2-STORY PUD - 1946 & NEWER": 160,
                                 "PUD - MULTILEVEL - INCL SPLIT LEV/FOYER": 180,
                                 "2 FAMILY CONVERSION - ALL STYLES AND AGES": 190}
     
    df['MS_SubClass'] = df['MS_SubClass'].replace(dict_subclass)
    df['MS_SubClass'] = df['MS_SubClass'].astype(int)
    
    df['Neighborhood'] = df['Neighborhood'].replace(dico_neigbhors)
    df['Neighborhood'] = df['Neighborhood'].astype(int)
    
    dict_po_to_ex = { 'Po': 0, 'Fa': 1, 'TA': 2, "Gd": 3, "Ex": 4 }
    df['Exter_Qual'] = df['Exter_Qual'].replace(dict_po_to_ex) 
    df['Exter_Qual'] = df['Exter_Qual'].astype(int)
    
    df['Kitchen_Qual'] = df['Kitchen_Qual'].replace(dict_po_to_ex) 
    df['Kitchen_Qual'] = df['Kitchen_Qual'].astype(int)
    
    df['condition_interieur'] = 1.8 * df['Overall_Cond'] + 2 * df['Overall_Qual'] + 0.6 * df['Kitchen_Qual'] 
    
    df['surface_total'] = df['surface_total'] +  df['BsmtFin_SF_first']
    
    df['main_score'] = df['Neighborhood'] * df['surface_total'] * df['condition_interieur']
    
    return df

# Preprocessing and features ingeneering 

df = pd.read_csv("model/data/AmesHousing.csv")
X_train, X_test, y_train, y_test = train_test_split(df, df.SalePrice, test_size=0.2, random_state=42)
neighbors_dict  = neighbors_and_conditions_dict(X_train)