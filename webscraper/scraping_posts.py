import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the CSV
df = pd.read_csv("export - export.csv")

# Base URL
base_url = "https://thecommononline.org"

# List to collect image URLs
image_urls = []

# Loop through each URL path in the spreadsheet
for relative_path in df["URL"]:
    if pd.isna(relative_path):
        image_urls.append("n/a")
        continue

    full_url = base_url + relative_path

    try:
        response = requests.get(full_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find('div', class_='post-media')
        if img_tag:
            img = img_tag.find('img')
            if img and img.get('src'):
                image_urls.append(img['src'])
            else:
                image_urls.append("n/a")
        else:
            image_urls.append("n/a")
    except Exception as e:
        image_urls.append("n/a")

# Add image URLs to the dataframe
df["Image URL"] = image_urls

# Save the updated dataframe to a new CSV file
df.to_csv("export_with_images.csv", index=False)
