import unittest
import pandas as pd
from modules.preprocessing import preprocess_data

class TestPreprocessing(unittest.TestCase):
    def test_preprocess_data_encoding(self):
        data = pd.DataFrame({
            'numeric': [1, 2, 3],
            'category': ['A', 'B', 'A']
        })
        processed_data = preprocess_data(data.copy())

        # Check if category is encoded to numbers (0 or 1)
        self.assertTrue(pd.api.types.is_numeric_dtype(processed_data['category']))
        self.assertEqual(len(processed_data['category'].unique()), 2)

if __name__ == '__main__':
    unittest.main()
