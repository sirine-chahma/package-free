import pandas as pd

#Data frame to store the locations
loc_df = pd.DataFrame({'id':['01', 'M01'], 'Name':['Nada', 'West End'],
                       'lat':[49.2638, 49.2828], 'lon':[-123.0895, -123.1302],
                       'shop':[1, 0]})

loc_df.to_csv('data/loc.csv')