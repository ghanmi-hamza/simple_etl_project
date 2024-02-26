import unittest
from unittest.mock import patch
from io import StringIO
from sqlalchemy import create_engine
from utils import extract_transform_load, json_serializable
from config import DATABASE_URL, DB_NAME, FOLDER_PATH
import pandas as pd

class TestUtils(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_extract_transform_load(self, mock_stdout):
        folder_path = FOLDER_PATH
        database_url = DATABASE_URL
        db_name = DB_NAME
        engine = create_engine(DATABASE_URL)

        with patch('os.listdir', return_value=['file1.csv']):
            with patch('pandas.read_csv', return_value=pd.DataFrame({"year_month": 2, "direction_code": "code12", "NA_area": "area1", "Count": 20,"geo_level":"a","period":"ab"}, index=[0])):
                extract_transform_load(folder_path, engine, db_name)

        expected_output = ""
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    def test_json_serializable(self):
        obj = [(202201, 'code1', 'area1', 10)]
        expected_result = [{"year_month": 202201, "direction_code": "code1", "NZ_area": "area1", "Count": 10}]
        self.assertEqual(json_serializable(obj), expected_result)

if __name__ == '__main__':
    unittest.main()