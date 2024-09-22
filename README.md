# RTA Transaction Extractor
This script is a simple automation for registered users of RTA (UAE) to download their transaction history into a CSV file. This script is handy due to the RTA 30 day transaction limit.

# Install
Requires [pipenv](https://pipenv.pypa.io/en/latest/) to be installed 

Run the following to clone the project and install the requirements
```bash
git clone git@github.com:i3130002/RTA_Transaction_Extractor.git
cd RTA_Transaction_Extractor
pipenv install
```

# Dependencies
You might need to install ffmpeg

`sudo apt-get install ffmpeg`


# Run
Run the following to run the script
```bash
pipenv run python main.py
```


# Youtube
Checkout this playlist to learn about how I made this script [here](https://www.youtube.com/playlist?list=PLtxitKIZCR4Ir0N2leUc4qPJd9OOHyvU0)