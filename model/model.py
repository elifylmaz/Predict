import numpy as np
import os

from sklearn.model_selection import train_test_split
from statsmodels.tools.sm_exceptions import ValueWarning
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, r2_score
import warnings

warnings.filterwarnings('ignore', category=ValueWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
def train_and_predict(df):
    models = {}
    mse_list = []
    r2_list = []

    for product_id in df['Product Id'].unique():
        product_data = df[df['Product Id'] == product_id]
        product_count = int(os.getenv('PRODUCT_COUNT'))

        if len(product_data) < product_count:
            #print(f"Product ID {product_id} has insufficient data.")
            continue

        X = product_data.drop(columns=['RequiredStock', 'Product Id'])
        y = product_data['RequiredStock']

        if y.isnull().any() or y.isin([np.inf, -np.inf]).any():
            #print(f"Product ID {product_id} contains missing or infinite values.")
            continue

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        y_train_mean = y_train.mean()
        y_train_std = y_train.std()
        y_train_normalized = (y_train - y_train_mean) / y_train_std
        y_test_normalized = (y_test - y_train_mean) / y_train_std

        try:
            model = ARIMA(y_train_normalized, order=(1, 1, 1))
            model_fit = model.fit()

            predictions_normalized = model_fit.forecast(steps=len(y_test_normalized))

            predictions = (predictions_normalized * y_train_std) + y_train_mean
            y_test = (y_test_normalized * y_train_std) + y_train_mean

            if np.isnan(predictions).any() or np.isnan(y_test).any():
                #print(f"NaN values found in predictions or y_test for Product ID {product_id}.")
                continue

            mse = mean_squared_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)

            mse_list.append(mse)
            r2_list.append(r2)

            models[product_id] = {
                'model': model_fit,
                'mse': mse,
                'r2': r2
            }

        except np.linalg.LinAlgError as e:
            print(f"Product ID {product_id} model training failed due to linear algebra error: {e}")

    avg_mse = np.mean(mse_list) if mse_list else None
    avg_r2 = np.mean(r2_list) if r2_list else None

    print(f'Average Mean Squared Error: {avg_mse}')
    print(f'Average R-squared: {avg_r2}')

    return models, avg_mse, avg_r2

