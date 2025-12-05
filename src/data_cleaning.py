#This file will be my main script, and it will clean the raw data with copilot and save it in another file
import pandas as pd
#This def will create the dataframe by reading the csv file
#We need to load the raw data into the pandas dataframe to deal with it
def load_data(file_path: str):
    return pd.read_csv(file_path)

#This def will clean the column names by removing spaces and converting them to lowercase
#Why: To ensure consistency and avoid issues when referencing column names
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.lower()
    return df

#This def will strip leading/trailing whitespace from text columns
#Why: Extra whitespace can cause duplicate entries and inconsistent data representation
def strip_whitespace(df):
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

#This def will handle missing values by either filling them or dropping them
#Why: Missing values can lead to inaccurate analysis and models
def handle_missing_values(df):
    df = df.dropna()
    return df

#This def will remove rows with invalid data based on certain criteria
#Why: Invalid data can skew results and lead to incorrect conclusions
def remove_invalid_rows(df):
    #Convert price and qty to numeric, replacing invalid values with NaN
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce').fillna(0).astype(int)
    #Drop rows with missing prices or quantities
    df = df.dropna()
    #Remove rows with negative prices (data entry errors)
    df = df[df['price'] >= 0]
    #Remove rows with negative quantities (impossible values)
    df = df[df['qty'] >= 0]
    return df

if __name__ == "__main__":
    raw_path = "Data/Raw/sales_data_raw.csv"
    cleaned_path = "Data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = strip_whitespace(df_clean)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())