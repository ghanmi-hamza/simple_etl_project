from flask import Flask, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy import text
from utils import extract_transform_load, json_serializable
from config import FOLDER_PATH, DATABASE_URL, DB_NAME
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
engine = create_engine(DATABASE_URL)

@app.route('/read/first-chunk', methods=['GET'])
def read_first_chunk():
    """ Returns the first 10 lines from Database """

    query_result = f"SELECT * FROM {DB_NAME} LIMIT 10"
    try:
        with engine.connect() as conn:
            query_result = conn.execute(text(query_result))
            conn.commit()
        result = json_serializable(query_result)
        logging.info("Successfully retrieved data from the database.")
        response = {
            "status": "success",
            "message": "A list of 10 JSON objects",
            "data": result
        }
        return make_response(jsonify(response),200)
    except Exception as e:
        logging.error(f"Error retrieving data from the database: {str(e)}")
        response = {
            "status": "failure",
            "message": "Failed to retrieve the data",
            "data": None
        }
        return make_response(jsonify(response), 400)


if __name__ == "__main__":
    extract_transform_load(FOLDER_PATH, engine,DB_NAME)
    app.run(debug=True)
