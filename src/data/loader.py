import pandas as pd
from pathlib import Path


def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV data into a pandas DataFrame.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        DataFrame containing the CSV data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        Exception: For other CSV parsing errors
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        raise Exception(f"Error reading CSV: {e}")