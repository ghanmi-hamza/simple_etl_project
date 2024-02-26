import os
import pandas as pd
import logging

logging.basicConfig(filename='etl.log', level=logging.INFO)

def extract_transform_load(folder_path:str, engine:str, db_name:str) -> None:
    """    Extracts data from CSV files in the specified folder, transforms it,
    and loads it into a database table"""
    #1. Extract and transform
    dataframes = []

    # List all files in the specified folder
    files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

    # Iterate over each CSV file in the folder
    for file in files:
        file_path = os.path.join(folder_path, file)
        try:
            logging.info(f"Successfully processed file: {file_path}")
            df = pd.read_csv(file_path)
            dataframes.append(df)
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {str(e)}")

    #2. Concatenate all dataframes
    transformed_data = pd.concat(dataframes)

    #3. Load to Database
    try:
        transformed_data.to_sql(db_name, engine, if_exists='replace', index=False)
        logging.info("Data successfully loaded to the database.")
    except Exception as e:
        logging.error(f"Error loading data to the database: {str(e)}")
    return

def json_serializable(obj) -> [dict]:
    """ serialize query result """
    res = []
    for row in obj:
        year_month, direction_code, NZ_area, Count, *_ = row
        row_data = {
                "year_month": year_month,
                "direction_code": direction_code,
                "NZ_area": NZ_area,
                "Count": Count
        }
        res.append(row_data)
    return res