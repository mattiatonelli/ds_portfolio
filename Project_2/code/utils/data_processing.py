import pandas as pd

def min_max_scaler(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform features by scaling each feature to a range from 0 to 1.
    """
    minimum = df.min()
    
    df = (df - minimum) / (df.max() - minimum)
    
    return df

def df_melter(y: pd.Series, df: pd.DataFrame) -> pd.DataFrame:
    """
    Modify the selected columns of a DataFrame from wide to long format.
    """
    df = pd.concat([y, df], axis=1)

    return pd.melt(df, id_vars='diagnosis', var_name='features', value_name='value')
