# ==========================================
# DATALENS AI - DATASET LOADER
# ==========================================

import pandas as pd


def load_dataset(file_path: str):

    """
    Load a CSV dataset and return it
    as a Pandas DataFrame.
    """

    try:

        df = pd.read_csv(file_path)

        print("Dataset loaded successfully.")

        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")

        return df

    except FileNotFoundError:

        print("Error: Dataset file not found.")

        return None

    except Exception as e:

        print(f"Error while loading dataset: {e}")

        return None