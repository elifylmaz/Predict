import pandas as pd
from dotenv import load_dotenv
from model.predict import predict_future
from model.preprocessing import df
from model.sarimax_model import models

load_dotenv()

def get_predictions(product_id):
    predictions_df=predict_future(models, df, pd.Timestamp.now())

    # Check if the product_id exists in the dataframe
    if int(product_id) not in predictions_df['Product Id'].values:
        return {'error': f'Product ID {product_id} does not exist in the predictions.'}

    # Get the predictions for the given product_id
    product_predictions = predictions_df[predictions_df['Product Id'] == int(product_id)].to_dict(orient='records')

    return {'predictions': product_predictions}
