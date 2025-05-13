import pandas as pd
import requests
from bs4 import BeautifulSoup
import re



def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def extract_from_post_body(full_url):
    # Parse HTML
    response = requests.get(full_url, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    post_body = soup.find('div', class_='post-body')
    if not post_body:
        print("no postbody")
        return None, None

    text = ''
    for elem in post_body:
        if isinstance(elem, str):
            text += elem
        elif hasattr(elem, 'get_text'):
            text += elem.get_text()
        if len(clean_text(text)) >= 1500:
            break

    cleaned = clean_text(text)
    after_300 = cleaned[300:]
    # Find the first period (".") to stop
    period_index = after_300.find('.')
    return after_300[:period_index+1], after_300[period_index+1: period_index + 200]

# Load the CSV
df = pd.read_csv("export - export.csv")

# Base URL
base_url = "https://thecommononline.org/"

# List to collect excerpts
excerpts = []

# Loop through each URL path in the spreadsheet
for relative_path in df["URL"]:
    if pd.isna(relative_path):
        excerpts.append("n/a")
        continue

    full_url = base_url + relative_path
    first_300, next_100 = extract_from_post_body(full_url)

    print("\nUntil period:\n", first_300)
    print("Next 100 characters:\n", next_100)

    # Cleaning text
    next_100 = next_100.lstrip()
    next_100 = re.sub(r'^[“”]', '', next_100)

    excerpts.append(next_100)

# Add excerpts to the dataframe
df["Excerpts"] = excerpts

# Save the updated dataframe to a new CSV file
df.to_csv("export_with_excerpts.csv", index=False)