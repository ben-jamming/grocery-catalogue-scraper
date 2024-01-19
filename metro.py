from calendar import c
import requests
from bs4 import BeautifulSoup
import time
import sqlite3

def scrape_page(url, conn):
    cursor = conn.cursor()
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            main_container = soup.find('div', class_="products-search--grid searchOnlineResults")
            if main_container:
                products = main_container.find_all('div', class_="default-product-tile tile-product item-addToCart")

                for product in products:
                    product_name = product.get('data-product-name', 'No Name')
                    product_category = product.get('data-product-category', 'No Category')
                    product_price = product.find('div', class_='pricing__sale-price')
                    product_id = product.get('data-product-code', 'No ID')

                    if product_price:
                        product_price = product_price.get_text(strip=True)
                    else:
                        product_price = 'No Price'
                        
                    cursor.execute('INSERT INTO products (product_name, category, price, product_id) VALUES (?, ?, ?, ?)', 
                                (product_name, product_category, product_price, product_id))
                                      
                    print(f'Product: {product_name}, Category: {product_category}, Price: {product_price}, ID: {product_id}')
                conn.commit()  
            else:
                print('Product container not found')
        else:
            print('Error occurred. Status code:', response.status_code)
    except Exception as e:
        print(f'An error occurred while scraping {url}:', str(e))
        conn.rollback()

if __name__ == '__main__':
    # Start with the first page
    conn = sqlite3.connect('grocery_items_db.db')
    base_url = 'https://www.metro.ca/en/online-grocery/search'
    current_page = 1
    pages_per_batch = 10
    while current_page < 268: # Assuming 267 is the last page
        page_url = f'{base_url}-page-{current_page}' if current_page > 1 else base_url
        print(f'Scraping page {current_page}')
        scrape_page(page_url, conn)

        # Increment the page
        current_page += 1

        # After every 10 pages, pause for 60 seconds
        if current_page % pages_per_batch == 0:
            print(f'Waiting 60 seconds before starting the next batch...')
            time.sleep(60)

    print('Scraping completed')
