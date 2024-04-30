# Price-Finder (insert emoji here)

### (insert emoji) Determine the resale value of hat lots with the help of computer vision.
Hats are one of the most popular item cateogires flipped on Ebay. Price Finder is an advanced computer vision application that leverages the YoloV8 object detection model, webscraping, and Ebay's developer API to accurately determine the potential resale value of individual hats within bulk hat lots found on Ebay. By utilizing Price Finder, ebay sellers can automate part of their sourcing workflow and increase their daily listing and sale rate. 

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
## Individual Hat Detection
The project employs object detection and tracking algorithms to identify and track the positions of players on the field throughout the game.
- Uses YOLOv8 Object Detection: Bounding box, classes, and segmentation

![Screenshot 2023-08-29 at 3 30 41 PM](https://github.com/SACUCD/SoccerOffsideTracker/assets/54915593/6a5fa29a-cd3d-4efa-b6dc-80440241b970)
***The small circle represents each players furthest body part. This is the point that is used for determining offsides***

*Note: Referee and Goalie are ignored*

## Aquiring Hat Lot Listings Through Webscrapping
The system also analyzes the colors of the player jerseys to distinguish between teams. By detecting the dominant colors on the players' uniforms, the algorithm can categorize them into teams.

- Uses bounding box to determine which way the player is facing
- Creates a smaller box at the most likely spot of the player's jersey
- Gets the average color in the smaller box
- Uses euclidean distance to group players into 3 groups: team1, team2, and team3 (referees and goalkeepers)

![Screenshot 2023-08-29 at 3 34 20 PM](https://github.com/SACUCD/SoccerOffsideTracker/assets/54915593/997e5746-d37a-40d5-bad7-ed487c5488ac)
***The smaller square represents the box used to determine the jersey color***

## Estimating the Price of Individual Hats
The most important part of this project is implementing perspective transform to get information on the actual distance down the field players are. This information is crucial for making offside determinations.

- Uses OpenCV's perspective transform
- Passes in each players furthest positioning (including any head, body, and feet) and places it on a 2D map of the field
- Determines who is nearest to the goal line and highlights that player

![Screenshot 2023-08-29 at 3 40 22 PM](https://github.com/SACUCD/SoccerOffsideTracker/assets/54915593/8b7bf324-b535-41a2-838f-3d49c8eca171)
***The red dots represents the points used for transforming the perspective***

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
