import os
from datetime import datetime
from dotenv import load_dotenv
from rta_extractor import RtaExtractor

# Inputs/ENV
load_dotenv()
RTA_USERNAME = os.getenv("RTA_USERNAME")
RTA_PASSWORD = os.getenv("RTA_PASSWORD")
NOL_CARD = os.getenv("RTA_NOL_CARD")

# Init
rta_extractor = RtaExtractor(RTA_USERNAME, RTA_PASSWORD, NOL_CARD)

# Step 1
rta_extractor.login()
# Step 2
rta_extractor.fill_form()

# Wait for the user to finish
input("Mark the captcha and fill it's challange, press next and let me know...")

# Step 3
travels = rta_extractor.get_travels()

# Enjoy the data
df = RtaExtractor.to_df(travels)

# Save it for later
date_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
df.to_csv(f"travel_history_{date_time}.csv", index=False)