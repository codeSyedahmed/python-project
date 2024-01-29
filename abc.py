import requests
from bs4 import BeautifulSoup

url = "https://www.ashford.com/brand/tissot.html"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract SKU information using a specific attribute name
    sku_elements = soup.find_all(attrs={'data-product-sku': True})

    # Extract price information using a specific class reference
    price_elements = soup.find_all(class_='price')

    for sku_element, price_element in zip(sku_elements, price_elements):
        # Get the values of the attributes
        sku_value = sku_element.get('data-product-sku')
        price_value = price_element.get_text(strip=True)
        print(f"SKU: {sku_value}, Price: {price_value}")
        print('-' * 30)

else:
    print(f"Failed to retrieve the webpage. Status Code: {response.status_code}")
