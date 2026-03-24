import pandas as pd
import re


#Load dataset
df = pd.read_csv("C:/Users/Lenovo/OneDrive/Desktop/sales dashboard/cleaned data.csv.txt")

print("Original Data:", df.head())

#Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")


#Clean text columns
text_cols = ["employee", "products", "region"]

for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.lower()

# Fix region consistency
df["region"] = df["region"].replace({
    "east": "East",
    "west": "West",
    "north": "North",
    "south": "South"
})

#Clean Unit Price
df["unit_price"] = df["unit_price"].astype(str)
df["unit_price"] = df["unit_price"].str.replace("Rs.", "", regex=False)
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

#Clean numeric columns with commas
def clean_number(x):
    if pd.isna(x):
        return None
    x = str(x)
    x = re.sub(r"[^\d]", "", x)  # remove everything except digits
    return int(x) if x != "" else None

cols_to_clean = ["cog", "total_sales", "profit"]

for col in cols_to_clean:
    df[col] = df[col].apply(clean_number)

#Convert Unit Sold
df["unit_sold"] = pd.to_numeric(df["unit_sold"], errors="coerce")

#Handle missing values
numeric_cols = ["unit_sold", "unit_price", "cog", "total_sales", "profit"]

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

#Remove duplicates
df = df.drop_duplicates()

#Fix date format
df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")

#Fix Total Sales (recalculate)
df["total_sales"] = df["unit_sold"] * df["unit_price"]


#fixing profit
df["profit"] = df["total_sales"] - df["cog"]

#Remove outliers (IQR)
for col in ["unit_sold", "unit_price", "total_sales"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    df = df[(df[col] >= lower) & (df[col] <= upper)]

#Final cleaned data
print("\nCleaned Data:\n", df.head())

print(" Data cleaned and saved successfully!")
