import pandas as pd
import os

def get_predictions(product_id):
    # predictions.json dosyasının varlığını kontrol et
    if not os.path.exists('predictions.json'):
        return {'error': 'Predictions file does not exist.'}

    # predictions.json dosyasını oku
    predictions_df = pd.read_json('predictions.json', lines=True)

    # product_id'nin dataframe'de olup olmadığını kontrol et
    if int(product_id) not in predictions_df['Product Id'].values:
        return {'error': f'Product ID {product_id} does not exist in the predictions.'}

    # Verilen product_id için tahminleri al
    product_predictions = predictions_df[predictions_df['Product Id'] == int(product_id)].to_dict(orient='records')

    return {'predictions': product_predictions}
