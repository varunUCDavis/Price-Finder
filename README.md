# Price-Finder 🤑

### Determine the resale value of hat lots with the help of computer vision 🧢
Hats are one of the most popular item cateogires flipped on Ebay. Price Finder is an advanced computer vision application that leverages the YoloV8 object detection model, webscraping, and Ebay's developer API to accurately determine the potential resale value of individual hats within bulk hat lots found on Ebay. By utilizing Price Finder, ebay sellers can automate part of their sourcing workflow and increase their daily listing and sale rate. 
#### Sample Output
![Image](https://drive.google.com/uc?export=view&id=1EWM1WPv4-tdzMwAK6SoxKyi9xLwHz_RW)


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

#### Ebay Developer Account 
To use Price Finder you need to have an approved eBay developer account. This step won't be neccessary in the future when the backend of the project is hosted.

1) Navigate to [https://developer.ebay.com/develop](https://developer.ebay.com/develop) and follow the instructions for setting up an account.
2) After creating your account follow [these steps](https://developer.ebay.com/api-docs/static/gs_create-the-ebay-api-keysets.html) to create an API keyset
3) Navigate to [Application keys](https://developer.ebay.com/my/keys) and copy down your Client ID and Client Secret<img src="https://drive.google.com/uc?export=view&id=1qTAbLir7zu1EqyH8BemNyskQCasb_Ghe" width="600">
4) Navigate to [User Access Tokens](https://developer.ebay.com/my/auth/?env=production&index=0) create a user token, and copy down your OAuth User Token <img src="https://drive.google.com/uc?export=view&id=1_N4pu1lnVVu9K9EoqSq0qN974eTzk5wA" width="800">

#### Chrome Webdriver
[Chrome webdriver](https://googlechromelabs.github.io/chrome-for-testing/) is needed inorder for the project to webscrape Ebay's website and aquire images of hat lots to analyze. After downloading the webdriver from the link above, unzip the file and copy down the absolute path to the webdriver. For example, "/Users/varunwadhwa/Downloads/chromedriver-mac-arm64/chromedriver"

### Installing and Running the Project

1. Clone the repo
   ```sh 
   git clone https://github.com/varunUCDavis/Price-Finder.git
   ```

2. Modify the following fields in `config.yaml` with your API and system path information 
   ```yaml
   chrome_driver_path: 'ENTER YOUR WEBDRIVER PATH'
   path: 'ENTER THE ABSOLUTE PATH TO YOUR PROJECT FOLDER'

   client_id: "ENTER YOUR CLIENT ID"
   client_sercret: "ENTER YOUR CLIENT SECRET"
   oauth_token: "ENTER YOUR OAUTH USER TOKEN"
   ```
3. Run the main.py script
   ```sh
   python main.py
   ```
#### Optional
The model being used to detect individual hats within the bulk lot images has already been trained. However, if you would like to add additional training data and retrain the model, follow these steps.
1) Add your training imgages and labels to "train/images" and "train/labels" respectively
2) Run the train.py script
   ```sh
   python train.py
   ```












# 🔑 Key Features
## Aquiring Hat Lot Listings Through Webscrapping
Inorder to obtain images of bulk lot hats to analyze for potential resale value, Selenium and Chrome Driver were used to search for hat lots on ebays website, and scrape the results page. 
```py
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

      # Download the image content
      response = requests.get(src)
      if response.status_code == 200:
          # Load the image content into an object that PIL can open
          image = Image.open(BytesIO(response.content)).convert('RGB')
          img_name = f"Lot{idx+1}"
          items[img_name] = [image, listing_href]

      # Go back to the search results page before proceeding to the next listing
      cls.driver.back()

  # Close the WebDriver
  cls.driver.quit()
  return items
```

## Individual Hat Detection
Inorder to detect individual hats from a bulk lot image, the yolov8 object detection model was augemnted with labeled images of hats. If the algorithm detects hats with a confidece level of above 65%, a bounding box is drawn with the predicted coordinates. 

![Screenshot 2023-08-29 at 3 30 41 PM](https://drive.google.com/uc?export=view&id=1rD8wMS-SUPzpRM02LOuMalEcYL1m0cdZ
)

## Estimating the Price of Individual Hats
After obtaining the images of individual hats from bulk lot imgaes, Ebay's image search API was used to find live listings of similar hats to each invidual hat. The first ten results of each search were used to estimate the potential selling price of the hat. The estimate was calculated by taking the first ten results' listing price, eliminating the outliers (outisde 1.5 IQR), and average the remaining results.  

```py
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
```

# 🪴 Areas of Improvement
- Reliability: The project could always have higher accuracy and reliability in offside decisions. It is only as accurate as the points it is given for perspective transform.
- Real-Time Video Analysis: The system would be more useful if it could process live video feeds from soccer matches, enabling real-time offside detection during gameplay.
- Pitch Detection: If the system could automatically detect and classify points on the field, the process would be entirely automated. This is a limitation created by non-fixed camera angles and could be solved with a fixed view of the field.
- Deep Sort: If players could be tracked throughout the game, we could implement automatic statistics on the amount of time spent offside.

# 🚀 Further Uses
- Team Formation Analysis: The project can further analyze the players' positions to determine the formation of each team during a particular play. This information can be valuable for understanding the dynamics of the game and how the offside decision impacts team strategies.
- Player Jersey Number Recognition: The system could utilize Optical Character Recognition (OCR) techniques to read the jersey numbers of players on the field. This allows the identification of individual players and track their movement and time spent offside.

# 💻  Technology
- OpenCV
- NumPy
- YoloV8
