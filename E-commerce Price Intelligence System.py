#Import all the required modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import numpy as np 
import os
#Scrape product data from the website
URL="https://books.toscrape.com/catalogue/category/books_1/index.html"
headers={"User-Agent":"Mozilla/5.0 (windows NT 10.0; Win64; x64)"}
response=requests.get(URL,headers=headers)
response.raise_for_status()
html=response.text
soup=BeautifulSoup(html,"html.parser")
products=soup.select("article.product_pod")
#Show HTML Structure
print(soup.prettify())
#Extract the required data and store it in a list
data=[]
for product in products:
    name=product.h3.a["title"]
    price=product.select_one("p.price_color").text.replace("$","")
    availability=product.select_one("p.instock.availability").text.strip()
    data.append({
        "Name":name,
        "Price":price,
        "Availability":availability
    })
#Store the data in a DataFrame and save it to a csv file
df=pd.DataFrame(data)
df["timestamp"]=datetime.now()
print(df.shape)
print(df.head())
df["scrape_date"]=datetime.now().date()
df.to_csv("rawdata_books.csv",index=False)
#Price Intelligence
df=pd.read_csv("rawdata_books.csv")
#Cleaning price column
df["Price"]=(df["Price"].astype(str)
             .str.replace("$","",regex=False))
df["Price"]=df["Price"].str.strip()
df["Price"]=pd.to_numeric(df["Price"],errors="coerce")
df=df.dropna(subset=["Price"])
#Compare prices overtime
df_sorted=df.sort_values(["Name","scrape_date"])
df_sorted["price_change"]=df_sorted.groupby("Name")["Price"].diff()
#Detect price drops
price_drops=df_sorted.loc[df_sorted["price_change"]<0]
#Numpy for price change analysis
avg_price=np.mean(df["Price"])
print(f"Average Price: ${avg_price:.2f}")
price_std=np.std(df["Price"])
print(f"Price Standard Deviation: ${price_std:.2f}")
#Reporting Export insights to a CSV file
os.makedirs("raw_data_books_processed",exist_ok=True)
df.to_excel("raw_data_books_processed/ptices.xlsx",index=False)
    

