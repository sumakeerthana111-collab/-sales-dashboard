# Sales Dashboard - Step 1: Data Cleaning
# Run this file first before any analysis

import pandas as pd
import numpy as np
import os

# ── Load Data ──────────────────────────────────────────────────────────────────
print("Loading dataset...")
df = pd.read_csv('../data/raw/superstore.csv', encoding='latin-1')
print(f"Raw data shape: {df.shape}")
print(df.head())

# ── Basic Info ─────────────────────────────────────────────────────────────────
print("\n--- Column Info ---")
print(df.dtypes)
print("\n--- Missing Values ---")
print(df.isnull().sum())

# ── Clean Data ─────────────────────────────────────────────────────────────────

# Remove duplicates
before = len(df)
df.drop_duplicates(inplace=True)
print(f"\nRemoved {before - len(df)} duplicate rows")

# Fix date columns
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date']  = pd.to_datetime(df['Ship Date'])

# Extract useful time features
df['Order Year']    = df['Order Date'].dt.year
df['Order Month']   = df['Order Date'].dt.month
df['Order Quarter'] = df['Order Date'].dt.quarter

# Add Profit Margin column
df['Profit Margin'] = (df['Profit'] / df['Sales']).round(4)

# Standardize text columns
df['Region']   = df['Region'].str.strip().str.title()
df['Category'] = df['Category'].str.strip().str.title()
df['Segment']  = df['Segment'].str.strip().str.title()

# ── Save Cleaned Data ──────────────────────────────────────────────────────────
os.makedirs('../data/cleaned', exist_ok=True)
df.to_csv('../data/cleaned/superstore_cleaned.csv', index=False)
print(f"\nCleaned data saved! Shape: {df.shape}")
print("Columns added: Order Year, Order Month, Order Quarter, Profit Margin")
