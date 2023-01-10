import mysql.connector
import requests
from bs4 import BeautifulSoup

def fetch_products():
    response = requests.get("http://www.-----.com/products")
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    for product_div in soup.find_all("div", class_="product"):
        name = product_div.find("h2").text
        price = float(product_div.find("span", class_="price").text[1:])
        image_url = product_div.find("img")["src"]
        products.append((name, price, image_url))
    return products

def update_database(products):
    cnx = mysql.connector.connect(user='<--->', password='<--->', host='<---->')
    cursor = cnx.cursor()
    cursor.execute("USE scraper_db")
    for name, price, image_url in products:
        cursor.execute("SELECT * FROM products WHERE name = %s AND price = %s", (name, price))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE products SET image_url = %s WHERE name = %s AND price = %s", (image_url, name, price))
        else:
            cursor.execute("INSERT INTO products (name, price, image_url) VALUES (%s, %s, %s)", (name, price, image_url))
    cnx.commit()
