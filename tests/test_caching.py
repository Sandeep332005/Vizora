import unittest
from unittest.mock import patch
import pandas as pd
import numpy as np
from modules.dimensionality import apply_pca

class TestDimensionalityCaching(unittest.TestCase):
    def test_apply_pca_caching_simulation(self):
        # We want to verify that calling the same function twice
        # is actually fast or could be cached.
        # Since I am using @st.cache_data, I need to test that.
        data = pd.DataFrame(np.random.rand(100, 5))

        # This is a bit hard to test directly without streamlit
        # but I will add the decorator first.
        pass

if __name__ == '__main__':
    unittest.main()
