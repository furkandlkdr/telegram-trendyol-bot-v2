import requests
from bs4 import BeautifulSoup
import re
from config import USER_AGENT
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def is_valid_trendyol_url(url):
    """Check if the URL is a valid Trendyol URL."""
    return bool(re.match(r'https?://(www\.)?(trendyol\.com|ty\.gl|tyml\.gl|trendyol-milla\.com).*', url))

def get_full_url(url):
    """Follow redirects to get the full URL if it's a shortened link."""
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.head(url, headers=headers, allow_redirects=True)
        return response.url
    except Exception as e:
        logger.error(f"Error following redirect for {url}: {e}")
        return url

def extract_price(text):
    """Extract numeric price value from text."""
    if not text:
        return None
    # Remove spaces and replace comma with dot
    price_text = text.strip().replace('.', '').replace(',', '.')
    # Extract numbers with decimal points using regex
    match = re.search(r'(\d+[,.]\d+|\d+)', price_text)
    if match:
        price = float(match.group(1).replace(',', '.'))
        # Add reasonable bounds check to avoid interpreting IDs as prices
        if 0.01 <= price <= 100000:  # Reasonable price range
            return price
    return None

def scrape_product_info(url):
    """Scrape product information from Trendyol."""
    try:
        # Follow redirects for shortened URLs
        full_url = get_full_url(url)
        
        # Check if the URL is a valid Trendyol URL
        if not is_valid_trendyol_url(full_url):
            return None, None, "URL does not belong to Trendyol"
        
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(full_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None, None, f"Failed to access the product page. Status code: {response.status_code}"
        
        soup = BeautifulSoup(response.text, 'lxml')
        # Extract product name from title
        title_tag = soup.find('title')
        product_name = title_tag.text.split('-')[0].strip() if title_tag else None
        
        # Try to get a better product name from h1 with class pr-new-br (Trendyol's product title class)
        h1_tag = soup.find('h1', class_='pr-new-br')
        if h1_tag:
            # If there's a brand link inside the h1
            brand_link = h1_tag.find('a', class_='product-brand-name-with-link')
            brand_name = brand_link.text.strip() if brand_link else ""
            
            # Find the span containing the product description
            product_desc_span = h1_tag.find('span')
            product_desc = product_desc_span.text.strip() if product_desc_span else ""
            
            # Combine brand and product description
            if brand_name and product_desc:
                product_name = f"{brand_name} {product_desc}"
            elif h1_tag.text:
                product_name = h1_tag.text.strip()
        
        # Fallback to any h1 tag if no specific product title tag found
        elif soup.find('h1'):
            product_name = soup.find('h1').text.strip()
        
        # Check if product is sold out
        sold_out_button = soup.select_one('.product-button-container .add-to-basket.sold-out')
        is_sold_out = False
        
        if sold_out_button and "Tükendi" in sold_out_button.text:
            is_sold_out = True
            logger.info(f"Product is sold out: {product_name}")
            return product_name, 0, "Tükendi"
        
        # Try different price selectors
        price = None
        price_selectors = [
            {"tag": "p", "class": "campaign-price"},
            {"tag": "span", "class": "prc-dsc"}
        ]
        
        for selector in price_selectors:
            price_tag = soup.find(selector["tag"], class_=selector["class"])
            if price_tag:
                price = extract_price(price_tag.text)
                if price:
                    break
        
        # If no price found with selectors, try JSON-LD data
        if not price:
            # Look for JSON-LD structured data which contains price information
            script_tags = soup.find_all('script', type='application/ld+json')
            for script in script_tags:
                try:
                    import json
                    data = json.loads(script.string)
                    if isinstance(data, dict) and 'offers' in data:
                        offers = data['offers']
                        if isinstance(offers, dict) and 'price' in offers:
                            price = float(offers['price'])
                            break
                except:
                    continue
        
        # If still no price, try JavaScript variables
        if not price:
            # Look for window variables containing price data
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and 'winnerVariant' in script.string:
                    # Extract price from winnerVariant data
                    import re
                    price_match = re.search(r'"price":\s*{\s*[^}]*"value":\s*([0-9.]+)', script.string)
                    if price_match:
                        price = float(price_match.group(1))
                        break
                    
        if not price:
            # Try to find any element containing TL as fallback (but be more careful)
            price_elements = soup.find_all(text=re.compile(r'\d+[,.]?\d*\s*TL|\d+[,.]?\d*\s*₺'))
            for element in price_elements:
                # Only extract if it looks like a price (not too large to be an ID)
                extracted_price = extract_price(element)
                if extracted_price and extracted_price < 100000:  # Reasonable price limit
                    price = extracted_price
                    break
        
        if not product_name:
            return None, None, "Could not extract product name"
            
        if not price:
            return product_name, None, "Could not extract price"
            
        return product_name, price, None
        
    except requests.RequestException as e:
        return None, None, f"Request error: {str(e)}"
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return None, None, f"Error scraping product: {str(e)}"

