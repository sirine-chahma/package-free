import pandas as pd

#Data frame to store the locations
loc_df = pd.DataFrame({'id': ['01', 'M01'], 'Name': ['Nada', 'West_End'],
                       'lat': [49.2638, 49.2828], 'lon': [-123.0895, -123.1302],
                       'shop': [1, 0], 'day': [[0, 1, 2, 3, 4, 5, 6], [1]]})

loc_df.to_csv('data/loc.csv')

food_df = pd.DataFrame({'id': ['01', 'M01', '01'],
                        'Name': ['Nada', 'West_End', 'Nada'],
                        'food': ['pasta', 'rice', 'rice'],
                        'min_price': [1.2, 4.5, 2],
                        'avg_price': [2, 5, 3],
                        'max_price': [4, 10, 4]})

food_df.to_csv('data/food.csv')



print(food_df.groupby(['id']))
