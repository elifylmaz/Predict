import pandas as pd
from scipy import stats
from dotenv import load_dotenv

load_dotenv()

def preprocess(data):

    if 'data' in data:
        data = data['data']
        print("Data preprocessing")
    df = pd.DataFrame(data)

    df['Date'] = pd.to_datetime(df['Date'], format='ISO8601')

    df['Month'] = df['Date'].dt.month.astype('int32')
    df['Season'] = (df['Month'] % 12 + 3) // 3
    df['Season'] = df['Season'].astype('int32')
    df['DayOfWeek'] = df['Date'].dt.dayofweek.astype('int32')
    df['Year'] = df['Date'].dt.year.astype('int32')

    df['Date'] = df['Date'].dt.strftime('%d.%m.%y')
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%y')

    df['Product Id'] = df['Product Id'].astype(str).apply(lambda x: int(x) if x.isdigit() else None)
    df = df.dropna(subset=['Product Id'])
    df['Product Id'] = df['Product Id'].fillna(0).astype('int32')

    df['NetProduct'] = (df['InputStockCount'] - df['OutputStockCount']).astype('int32')
    df.drop(columns=['InputStockCount', 'OutputStockCount', 'Stock'], inplace=True)

    df['MonthlyMeans'] = df.groupby(['Product Id', 'Month'])['NetProduct'].transform('mean').astype('int32')
    df['SeasonalMeans'] = df.groupby(['Product Id', 'Season'])['NetProduct'].transform('mean').astype('int32')

    df['RequiredStock'] = df['MonthlyMeans'] + df['NetProduct']

    z_scores = stats.zscore(df[['NetProduct', 'MonthlyMeans', 'SeasonalMeans', 'RequiredStock']])
    abs_z_scores = abs(z_scores)
    filtered_entries_z = (abs_z_scores < 3).all(axis=1)
    df = df[filtered_entries_z]

    Q1 = df[['NetProduct', 'MonthlyMeans', 'SeasonalMeans', 'RequiredStock']].quantile(0.25)
    Q3 = df[['NetProduct', 'MonthlyMeans', 'SeasonalMeans', 'RequiredStock']].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df = df[~((df[['NetProduct', 'MonthlyMeans', 'SeasonalMeans', 'RequiredStock']] < lower_bound) | (
                df[['NetProduct', 'MonthlyMeans', 'SeasonalMeans', 'RequiredStock']] > upper_bound)).any(axis=1)]

    df.set_index('Date', inplace=True)

    df.sort_index(inplace=True)

    return df
