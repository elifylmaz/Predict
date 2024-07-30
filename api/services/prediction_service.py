import pandas as pd
import os

def get_predictions(product_id):
    if not os.path.exists('predictions.json'):
        return {'error': 'Predictions file does not exist.'}

    predictions_df = pd.read_json('predictions.json', lines=True)

    if int(product_id) not in predictions_df['Product Id'].values:
        return {'error': f'Product ID {product_id} does not exist in the predictions.'}

    product_predictions = predictions_df[predictions_df['Product Id'] == int(product_id)].to_dict(orient='records')

    return {'predictions': product_predictions}
