import base64
import io
import requests
import yaml
from PIL import Image


class PriceFinder:

    with open("config.yaml", 'r') as file:
        config = yaml.safe_load(file)

    # Replace these with your actual eBay API credentials
    CLIENT_ID = config['client_id']
    CLIENT_SECRET = config['client_secret']
    OAUTH_TOKEN = config['oauth_token']

    # eBay Browse API endpoint for image search
    API_ENDPOINT = 'https://api.ebay.com/buy/browse/v1/item_summary/search_by_image?&limit=10&conditions=USED'

    # Path to your image file
    IMAGE_PATH = '/Users/varunwadhwa/Desktop/ebayScrapper2/image4.png'

    # Prepare the headers
    headers = {
        'Authorization': f'Bearer {OAUTH_TOKEN}',
        'X-EBAY-C-MARKETPLACE-ID': 'EBAY_US',
        'X-EBAY-C-ENDUSERCTX': 'affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>',
        'Content-Type': 'application/json'
        
    }
    filters = 'sold:true,conditions:USED'


    @classmethod
    def mean_without_outliers(cls, data):
        import numpy as np
        
        # Calculate Q1 (25th percentile) and Q3 (75th percentile)
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        
        # Calculate the Interquartile Range (IQR)
        IQR = Q3 - Q1
        
        # Define outliers as those outside of Q1 - 1.5 * IQR and Q3 + 1.5 * IQR
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Filter out outliers and calculate the mean of the remaining data
        filtered_data = [x for x in data if lower_bound <= x <= upper_bound]
        
        # Return the mean of the filtered data
        if filtered_data:  # Check if the list is not empty
            return np.mean(filtered_data)
        else:
            return None  # Return None if all data are outliers or list is empty

    @classmethod
    def find_prices(cls, img):
        prices = []
        # Prepare the payload with the base64-encoded image
        payload = {
            'image': base64.b64encode(img).decode('utf-8')
        }

        # Make the POST request to the eBay API
        response = requests.post(cls.API_ENDPOINT, headers=cls.headers, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response data
            items = response.json()
            # Check if any items found
            if 'itemSummaries' in items and len(items['itemSummaries']) > 0:
                for item in items['itemSummaries']:
                    prices.append(float(item['price']['value']))
                return cls.mean_without_outliers(prices)
            else:
                print("No items found.")
        else:
            print("Failed to search by image. Status code:", response.status_code, "Response:", response.text)

