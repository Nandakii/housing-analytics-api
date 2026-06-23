import pandas as pd
import sqlite3

print("Loading massive CSV... hang tight...")
df = pd.read_csv("HousingDataset.csv")

print("Cleaning columns and dropping null values...")
df = df.drop(['ad_type', 'title', 'description', 'l4', 'l5', 'l6'], axis=1, errors='ignore')
df = df.dropna(subset=['lon', 'lat', 'price_period', 'bedrooms', 'surface_total', 'rooms', 'price', 'surface_covered'])

print("Splitting into normalized dataframes...")
property_details = df[['id', 'start_date', 'end_date', 'created_on', 'lat', 'lon', 'l1', 'l2', 'l3', 'rooms', 'bedrooms', 'bathrooms', 'surface_total', 'surface_covered']]
property_price_details = df[['id', 'price', 'currency', 'price_period', 'property_type', 'operation_type']]

print("Writing directly to SQLite binary database...")
conn = sqlite3.connect('housing_dataset.sqlite')
property_details.to_sql('property_details', conn, index=False, if_exists='replace')
property_price_details.to_sql('property_price_details', conn, index=False, if_exists='replace')
conn.close()

print("SUCCESS! 'housing_dataset.sqlite' has been created locally!")
