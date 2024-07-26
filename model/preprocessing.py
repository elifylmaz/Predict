import pandas as pd
from scipy import stats
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

def preprocess(data):

    if 'data' in data:
        data = data['data']
        print("Data preprocessing")
    df = pd.DataFrame(data)

    # Preprocess
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='ISO8601')

    # Calculate 'Month', 'Season', 'DayOfWeek' and 'Year'
    df['Month'] = df['Date'].dt.month.astype('int32')
    df['Season'] = (df['Month'] % 12 + 3) // 3
    df['Season'] = df['Season'].astype('int32')
    df['DayOfWeek'] = df['Date'].dt.dayofweek.astype('int32')
    df['Year'] = df['Date'].dt.year.astype('int32')

    # Convert 'Date' to %d.%m.%y format
    df['Date'] = df['Date'].dt.strftime('%d.%m.%y')
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%y')

    # Convert 'Product ID' column to integer, handle NaN values
    df['Product Id'] = df['Product Id'].astype(str).apply(lambda x: int(x) if x.isdigit() else None)
    df = df.dropna(subset=['Product Id'])  # Drop rows where 'Product ID' is NaN
    df['Product Id'] = df['Product Id'].fillna(0).astype('int32')  # Replace NaN values in 'Product ID' with 0 and convert to int

    # Calculate 'NetProduct' as difference between 'InputStockCount' and 'OutputStockCount'
    df['NetProduct'] = (df['InputStockCount'] - df['OutputStockCount']).astype('int32')
    df.drop(columns=['InputStockCount', 'OutputStockCount', 'Stock'], inplace=True)

    # Calculate 'MonthlyMeans' and 'SeasonalMeans' per product
    df['MonthlyMeans'] = df.groupby(['Product Id', 'Month'])['NetProduct'].transform('mean').astype('int32')
    df['SeasonalMeans'] = df.groupby(['Product Id', 'Season'])['NetProduct'].transform('mean').astype('int32')

    # Calculate the required stock level
    df['RequiredStock'] = df['MonthlyMeans'] + df['NetProduct']  # This is just a placeholder for illustration

    # Outlier Detection and Cleaning

    # Outlier detection using z-score method
    z_scores = stats.zscore(df[['NetProduct', 'MonthlyMeans', 'SeasonalMeans', 'RequiredStock']])
    abs_z_scores = abs(z_scores)
    filtered_entries_z = (abs_z_scores < 3).all(axis=1)
    df = df[filtered_entries_z]

    # Outlier detection using IQR method
    Q1 = df[['NetProduct', 'MonthlyMeans', 'SeasonalMeans', 'RequiredStock']].quantile(0.25)
    Q3 = df[['NetProduct', 'MonthlyMeans', 'SeasonalMeans', 'RequiredStock']].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    df = df[~((df[['NetProduct', 'MonthlyMeans', 'SeasonalMeans', 'RequiredStock']] < lower_bound) | (
                df[['NetProduct', 'MonthlyMeans', 'SeasonalMeans', 'RequiredStock']] > upper_bound)).any(axis=1)]

    # Set the Date column as the index
    df.set_index('Date', inplace=True)

    # Sort the index by date
    df.sort_index(inplace=True)

    # Return the processed DataFrame
    return df
