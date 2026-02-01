#Import the required library
import requests
from bs4 import BeautifulSoup
import pandas as pd
#Extract the required data 
URL="https://books.toscrape.com/catalogue/category/books_1/index.html"
headers={"User-Agent":"Mozilla/5.0(Windows NT 10.0;Win64; x64)"}
response=requests.get(URL,headers=headers)
response.raise_for_status()
html=response.text
books_data=[]
for page in range(1,51): #50 Pages Total
    print(f"Scraping page{page}...")
    url=URL.format(page)
    if response.status_code!=200:
        print("Failed to retrive page")
        continue
soup=BeautifulSoup(response.text,"html.parser")
#Show HTML Structure
print(soup.prettify())
books=soup.find_all("article",class_="product_pod")
for book in books:
    title=book.h3.a["title"]
    price=book.find("p",class_="price_color").text
    availability=book.find("p",class_="instock availability").text.strip()
    rating=book.find("p",class_="star-rating")["class"][1]
    book_url=book.h3.a["href"]
    books_data.append({
        "Title":title,
        "Price":price,
        "Availability":availability,
        "Rating":rating,
        "Book URL":"https://books.toscrape.com/catalogue/"+book_url})
#Create a DataFrame    
df=pd.DataFrame(books_data)
#Save data
df.to_csv("books_data.csv",index=False)
print("\nScraping Completed!!")
print(df.head())

    