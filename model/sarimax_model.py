import numpy as np
import os
from statsmodels.tools.sm_exceptions import ValueWarning
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from model.preprocessing import df
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
        product_count = int(os.getenv('PRODUCT_COUNT'))  # Default to 30 if not set

        if len(product_data) < product_count:
            #print(f"Product ID {product_id} has insufficient data.")
            continue

        # Prepare data
        X = product_data.drop(columns=['RequiredStock', 'Product Id'])
        y = product_data['RequiredStock']

        # Check for missing or infinite values
        if y.isnull().any() or y.isin([np.inf, -np.inf]).any():
            #print(f"Product ID {product_id} contains missing or infinite values.")
            continue

        # Splitting the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Normalize the target variable
        y_train_mean = y_train.mean()
        y_train_std = y_train.std()
        y_train_normalized = (y_train - y_train_mean) / y_train_std
        y_test_normalized = (y_test - y_train_mean) / y_train_std

        try:
            # Train ARIMA model
            model = ARIMA(y_train_normalized, order=(1, 1, 1))
            model_fit = model.fit()

            # Forecasting
            predictions_normalized = model_fit.forecast(steps=len(y_test_normalized))

            # Denormalize the predictions
            predictions = (predictions_normalized * y_train_std) + y_train_mean
            y_test = (y_test_normalized * y_train_std) + y_train_mean

            # Check for NaN values in predictions and y_test
            if np.isnan(predictions).any() or np.isnan(y_test).any():
                #print(f"NaN values found in predictions or y_test for Product ID {product_id}.")
                continue

            # Evaluate the model
            mse = mean_squared_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)

            mse_list.append(mse)
            r2_list.append(r2)

            # Save model and metrics
            models[product_id] = {
                'model': model_fit,
                'mse': mse,
                'r2': r2
            }

        except np.linalg.LinAlgError as e:
            print(f"Product ID {product_id} model training failed due to linear algebra error: {e}")

    # Calculate average MSE and R2
    avg_mse = np.mean(mse_list) if mse_list else None
    avg_r2 = np.mean(r2_list) if r2_list else None

    print(f'Average Mean Squared Error: {avg_mse}')
    print(f'Average R-squared: {avg_r2}')

    return models, avg_mse, avg_r2


models, avg_mse, avg_r2 = train_and_predict(df)
