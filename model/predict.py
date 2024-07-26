import calendar
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_season_name(season_number):
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Autumn', 4: 'Winter'}
    return season_mapping.get(season_number, f'Season {season_number}')

def predict_future(models, data, current_date):
    predictions = []

    current_month = current_date.month
    current_season = (current_month % 12 + 3) // 3

    for product_id, model_info in models.items():
        model_fit = model_info['model']
        product_data = data[data['Product Id'] == product_id]

        # Prepare data for the next 3 months
        next_3_months_preds = model_fit.forecast(steps=3).tolist()

        # Prepare data for the next 2 seasons
        next_2_seasons_preds = model_fit.forecast(steps=6).tolist()[3:5]

        # Convert month number to name
        current_month_name = calendar.month_name[current_month]

        # Determine next month and next 2 months
        if current_month == 12:
            next_month_name = calendar.month_name[1]
            next_2_months_name = calendar.month_name[2]
        else:
            next_month_name = calendar.month_name[current_month + 1]
            if current_month == 11:
                next_2_months_name = calendar.month_name[1]
            else:
                next_2_months_name = calendar.month_name[current_month + 2]

        # Determine next 2 seasons
        next_season = (current_season + 1 - 1) % 4 + 1
        next_2_season = (current_season + 2 - 1) % 4 + 1

        predictions.append({
            'Product Id': product_id,
            f'{current_month_name}': round(next_3_months_preds[0], 2) if len(next_3_months_preds) > 0 else 0.0,
            f'{next_month_name}': round(next_3_months_preds[1], 2) if len(next_3_months_preds) > 1 else 0.0,
            f'{next_2_months_name}': round(next_3_months_preds[2], 2) if len(next_3_months_preds) > 2 else 0.0,
            get_season_name(current_season): round(next_2_seasons_preds[0], 2) if len(next_2_seasons_preds) > 0 else 0.0,
            get_season_name(next_season): round(next_2_seasons_preds[1], 2) if len(next_2_seasons_preds) > 1 else 0.0
        })

    # Create a DataFrame for predictions
    predictions_df = pd.DataFrame(predictions)

    # Save the DataFrame to a CSV file
    #predictions_df.to_csv('predictions.csv', index=False)

    return predictions_df
