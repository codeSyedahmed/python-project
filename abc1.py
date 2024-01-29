import requests
from bs4 import BeautifulSoup
import random

# List of URLs to scrape
urls = [
    "https://www.ashford.com/brand/glycine.html"
]

# Markup multiplier
markup_multiplier = 1.2  # You can adjust this value as needed

# Preloaded list of SKUs
#preloaded_skus = set(["123", "456", "789"])  # Add your SKUs here

# Output file name
output_file = "output.csv"

def calculate_marked_up_price(price):
    return (price * markup_multiplier) + 10

def scrape_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        sku_elements = soup.find_all(attrs={'data-product-sku': True})
        price_elements = soup.find_all(class_='price')

        scraped_data = []

        for sku_element, price_element in zip(sku_elements, price_elements):
            sku = sku_element.get('data-product-sku')
            price = float(price_element.get_text(strip=True).replace('$', '').replace(',', ''))
            marked_up_price = calculate_marked_up_price(price)
            scraped_data.append((sku, marked_up_price, 1))

        return scraped_data

    return []

def main():
    all_data = []

    for url in urls:
        data = scrape_data(url)
        all_data.extend(data)

    # Write data to output file
    with open(output_file, 'w') as f:
        f.write("SKU PRICE QUANTITY\n")
        
        for sku, marked_up_price, quantity in all_data:
            f.write(f"{sku} {marked_up_price:.2f} {quantity}\n")

        # Add SKUs not scraped
        for sku in preloaded_skus:
            if sku not in [item[0] for item in all_data]:
                f.write(f"{sku} 100.00 0\n")  # Assign a random price (e.g., 100) and quantity 0

if __name__ == "__main__":
    main()
