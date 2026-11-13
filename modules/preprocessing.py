import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

def preprocess_data(df):
    """Preprocessing: encode categorical, impute missing, and scale numeric."""
    # 1. Encode categorical columns
    le = LabelEncoder()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        df[col] = le.fit_transform(df[col].astype(str))

    # 2. Separate numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns

    # 3. Impute missing values
    imputer = SimpleImputer(strategy='mean')
    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

    # 4. Scale numeric
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df
