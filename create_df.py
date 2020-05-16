import pandas as pd

#Data frame to store the locations
loc_df = pd.DataFrame({'id': ['01', 'M01'], 'Name': ['Nada', 'West_End'],
                       'lat': [49.2638, 49.2828], 'lon': [-123.0895, -123.1302],
                       'shop': [1, 0], 'day': ['{0, 1, 2, 3, 4, 5, 6}', {1}]})

loc_df.to_csv('data/loc.csv')

open_days_int = [0, 2]

loc_df['is_open'] = list(map(lambda x: not set(x).isdisjoint(open_days_int), loc_df['day']))

loc_df = loc_df[loc_df['is_open']]

print(loc_df)



