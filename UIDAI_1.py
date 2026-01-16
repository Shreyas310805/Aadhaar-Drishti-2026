import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set(style="whitegrid")

# Load the datasets (Replace with your actual filenames)
# Assuming files are CSVs. If they are Excel, use pd.read_excel()
try:
    # Use the filenames visible in your sidebar
    df_enrolment = pd.read_csv('DataSet1.csv')
    df_demographic = pd.read_csv('DataSet2.csv')
    # df_biometric = pd.read_csv('DataSet3.csv') # Uncomment if you need this
    
    print("Files loaded successfully!")
    
    # Move these INSIDE the try block
    print("Enrolment Data Head:")
    print(df_enrolment.head())

except FileNotFoundError:
    print("Error: The files were not found. Check the names in the sidebar!")
# Quick look at the data
print("Enrolment Data Head:")
print(df_enrolment.head())
# Function to get a summary of missing data
def check_missing(df, name):
    print(f"--- Missing Values in {name} ---")
    print(df.isnull().sum())
    print("\n")

check_missing(df_enrolment, "Enrolment")
check_missing(df_demographic, "Demographic Updates")

# Standardize Date Columns (CRITICAL STEP)
# Replace 'Date' with the actual column name in your dataset
# df_enrolment['Date'] = pd.to_datetime(df_enrolment['Date'])