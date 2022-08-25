import pandas as pd
import pickle
base_path = "data/"
# Load data
with open(base_path + 'data.pkl', 'rb') as fr:
    data = pickle.load(fr)

data_df = pd.DataFrame(data)


data_df = data_df.fillna('없음')

temp = pd.DataFrame(data_df.iloc[:, 2].str.split(expand=True)[1].value_counts())
# temp.to_csv('city_count_list_2.csv', encoding='utf-8')
print(
    
    data_df

    )