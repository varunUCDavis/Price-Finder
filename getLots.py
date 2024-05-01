import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
from PIL import Image
import yaml

class Lots:

    EBAYLINK = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1312&_nkw=sports+hat+lot&_sacat=0&_pgn=2"
    #SAVEDIR = "HatLots"
    NUMIMAGES = 5

    with open("config.yaml", 'r') as file:
        config = yaml.safe_load(file)
    # ChromeDriver path
    chrome_driver_path = config['chrome_driver_path']
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    @classmethod
    def getLots(cls) -> dict:
        items = {}
        cls.driver.get(cls.EBAYLINK)
        # Get all listing elements
        # Wait for the page to load and the elements to be present
        wait = WebDriverWait(cls.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'srp-river-results')))
        listings = cls.driver.find_elements(By.CSS_SELECTOR, "#srp-river-results .s-item__link")
        listing_hrefs = [listing.get_attribute('href') for listing in listings]

        # Loop through each listing link
        for idx, listing_href in enumerate(listing_hrefs[:cls.NUMIMAGES]):  # Limiting to the first 10 listings for this example
            # Open the listing page
            cls.driver.get(listing_href)
            
            # Now on the listing page, wait for the main image to load and then scrape it
            main_image = cls.driver.find_element(By.CSS_SELECTOR, "div.ux-image-carousel-item.image-treatment.active.image img")
            src = main_image.get_attribute('src')
            item_price = cls.driver.find_element(By.CSS_SELECTOR, "div.x-price-primary span").text
            dollar_index = item_price.find('$')
            item_price = float(item_price[dollar_index+1:])
            shipping_price = cls.driver.find_element(By.CSS_SELECTOR, "div.vim.d-shipping-minview.mar-t-20").find_element(By.CSS_SELECTOR, "div.ux-labels-values__values-content").find_element(By.CSS_SELECTOR, "span.ux-textspans").text
            if "Free" in shipping_price:
                shipping_price = 0
            else:
                dollar_index = shipping_price.find('$')
                shipping_price = float(shipping_price[dollar_index+1:])
            item_price += shipping_price
            # Download the image content
            response = requests.get(src)
            if response.status_code == 200:
                # Load the image content into an object that PIL can open
                image = Image.open(BytesIO(response.content)).convert('RGB')
                img_name = f"Lot{idx+1}"
                items[img_name] = [image, listing_href, item_price]

            # Go back to the search results page before proceeding to the next listing
            cls.driver.back()

        # Close the WebDriver
        cls.driver.quit()
        return items

