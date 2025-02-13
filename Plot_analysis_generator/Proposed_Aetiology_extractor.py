import requests
from bs4 import BeautifulSoup
import argparse
import os

# Define argument parser
parser = argparse.ArgumentParser(description="Fetch SBS aetiologies and save HTML pages.")
parser.add_argument("-l", "--list", required=True, help="Path to the text file containing SBS signatures (one per line).")
args = parser.parse_args()

# Read the SBS list from the file
with open(args.list, "r") as file:
    sbs_list = [line.strip() for line in file.readlines() if line.strip()]

base_url = "https://cancer.sanger.ac.uk/signatures/sbs/{}"

def extract_aetiology_from_html(filename):
    """Extracts aetiology from the 'Proposed aetiology' section before 'Acceptance criteria'."""
    with open(filename, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Locate the "Proposed aetiology" and "Acceptance criteria" headers
    start = soup.find(lambda tag: tag.name in ["h3", "h2"] and "Proposed aetiology" in tag.text)
    end = soup.find(lambda tag: tag.name in ["h3", "h2"] and "Acceptance criteria" in tag.text)

    if start and end:
        content = []
        for elem in start.find_next_siblings():
            if elem == end:
                break
            if elem.name not in ["script", "style"]:  # Ignore scripts and styles
                content.append(elem.get_text(separator=" ", strip=True))
        return " ".join(content) if content else "Unknown"
    
    return "Unknown"

def fetch_aetiology(sbs):
    url = base_url.format(sbs.lower())  # Convert SBS to lowercase
    response = requests.get(url)

    if response.status_code == 200:
        print(f"✅ Found {sbs} at {url}")

        # Save the HTML page
        filename = f"{sbs}.html"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"📄 Saved {sbs} page as {filename}")

        # Extract the first aetiology using BeautifulSoup
        aetiology = extract_aetiology_from_html(filename)

        # Extract full aetiology (Associated Aetiology)
        soup = BeautifulSoup(response.text, "html.parser")
        aetiology_td = soup.find("td", {"headers": "aet1"})
        associated_aetiology = aetiology_td.get_text(separator=" ", strip=True) if aetiology_td else "Unknown"

        # Print the extracted details
        print(f"{sbs} Aetiology: {aetiology}\n")
        print(f"{sbs} Seccond Aetiology: {associated_aetiology}\n")
    else:
        print(f"❌ Could not retrieve {sbs}. Status code: {response.status_code}")
    print ("-----------------------------------------------------------------------------------------------------------")

# Loop through each SBS signature
for sbs in sbs_list:
    fetch_aetiology(sbs)
