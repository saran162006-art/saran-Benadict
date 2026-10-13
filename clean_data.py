import pandas as pd
import numpy as np

df = pd.read_csv('/home/claude/movies_project/movies_raw.csv')

print("=" * 60)
print("BEFORE CLEANING")
print("=" * 60)
print(f"Shape: {df.shape}")
print(f"Duplicates: {df.duplicated().sum()}")
print(f"Missing values:\n{df.isna().sum()}")

# ---------- 1. Remove exact duplicate rows ----------
df = df.drop_duplicates().reset_index(drop=True)

# ---------- 2. Standardize text columns (Genre, Country) ----------
df['Genre'] = df['Genre'].str.strip().str.title()
df['Genre'] = df['Genre'].replace({'Sci Fi': 'Sci-Fi', 'Sci-Fi': 'Sci-Fi'})

country_map = {
    'usa': 'USA', 'U.S.A': 'USA', 'USA': 'USA',
    'india': 'India', 'India': 'India',
    'U.K.': 'UK', 'Uk': 'UK', 'UK': 'UK'
}
df['Country'] = df['Country'].replace(country_map)
df['Country'] = df['Country'].str.strip()

# ---------- 3. Handle missing values ----------
# Numeric columns -> fill with median (robust to outliers)
for col in ['Duration_Min', 'Rating', 'Votes', 'Budget_Million', 'Revenue_Million']:
    median_val = df[col].median()
    df[col] = df[col].fillna(median_val)

# Categorical -> fill with mode / 'Unknown'
df['Director'] = df['Director'].fillna('Unknown')
df['Country'] = df['Country'].fillna(df['Country'].mode()[0])

# Year -> fill missing with median year (rounded, int)
df['Year'] = df['Year'].fillna(df['Year'].median())
df['Year'] = df['Year'].astype(int)

# ---------- 4. Handle outliers using IQR capping ----------
def cap_outliers_iqr(series, factor=1.5):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    return series.clip(lower=lower, upper=upper)

for col in ['Duration_Min', 'Budget_Million', 'Revenue_Million', 'Votes']:
    df[col] = cap_outliers_iqr(df[col])

# Round numeric columns for readability
df['Duration_Min'] = df['Duration_Min'].round(0).astype(int)
df['Votes'] = df['Votes'].round(0).astype(int)
df['Budget_Million'] = df['Budget_Million'].round(2)
df['Revenue_Million'] = df['Revenue_Million'].round(2)
df['Rating'] = df['Rating'].round(1)

# ---------- 5. Feature engineering ----------
df['Profit_Million'] = (df['Revenue_Million'] - df['Budget_Million']).round(2)
df['ROI_Percent'] = ((df['Profit_Million'] / df['Budget_Million']) * 100).round(1)
df['Decade'] = (df['Year'] // 10 * 10).astype(str) + 's'

print("\n" + "=" * 60)
print("AFTER CLEANING")
print("=" * 60)
print(f"Shape: {df.shape}")
print(f"Duplicates: {df.duplicated().sum()}")
print(f"Missing values:\n{df.isna().sum()}")
print(f"\nGenre categories: {sorted(df['Genre'].unique())}")
print(f"Country categories: {sorted(df['Country'].unique())}")

df.to_csv('/home/claude/movies_project/movies_cleaned.csv', index=False)
print("\nCleaned dataset saved -> movies_cleaned.csv")
