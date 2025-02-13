import requests
from bs4 import BeautifulSoup
import argparse
import os

class SBSScraper:
    """Class to fetch SBS aetiologies and save HTML pages."""

    BASE_URL = "https://cancer.sanger.ac.uk/signatures/sbs/{}"

    def __init__(self, sbs_list_file):
        self.sbs_list = self.load_sbs_list(sbs_list_file)

    @staticmethod
    def load_sbs_list(file_path):
        """Reads the SBS list from a file."""
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines() if line.strip()]

    @staticmethod
    def extract_aetiology_from_html(filename):
        """Extracts aetiology from the 'Proposed aetiology' section before 'Acceptance criteria'."""
        with open(filename, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        start = soup.find(lambda tag: tag.name in ["h3", "h2"] and "Proposed aetiology" in tag.text)
        end = soup.find(lambda tag: tag.name in ["h3", "h2"] and "Acceptance criteria" in tag.text)

        if start and end:
            content = []
            for elem in start.find_next_siblings():
                if elem == end:
                    break
                if elem.name not in ["script", "style"]:
                    content.append(elem.get_text(separator=" ", strip=True))
            aetiology_text = " ".join(content) if content else "Unknown"
            if "Comments" in aetiology_text:
                aetiology_text = aetiology_text.replace("Comments", "\n***Comments:")
            return aetiology_text
        
        return "Unknown"
    
    @staticmethod
    def extract_associated_signatures_from_html(filename):
        """Extracts associated signatures between 'Associated signatures' and 'Replication timing'."""
        with open(filename, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        start = soup.find(lambda tag: tag.name in ["h3", "h2"] and "Associated signatures" in tag.text)
        end = soup.find(lambda tag: tag.name in ["h3", "h2"] and "Replication timing" in tag.text)

        if start and end:
            content = []
            for elem in start.find_next_siblings():
                if elem == end:
                    break
                if elem.name not in ["script", "style"]:
                    content.append(elem.get_text(separator=" ", strip=True))
            return " ".join(content) if content else "Unknown"
        
        return "Unknown"
    
    def fetch_aetiology(self, sbs):
        """Fetches SBS signature aetiology and saves the HTML file."""
        url = self.BASE_URL.format(sbs.lower())
        response = requests.get(url)

        if response.status_code == 200:
            print(f"✅ Found {sbs} at {url}")

            # Save the HTML page
            filename = f"{sbs}.html"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"📄 Saved {sbs} page as {filename}")

            # Extract aetiology
            aetiology = self.extract_aetiology_from_html(filename)

            # Extract associated signatures
            associated_signatures = self.extract_associated_signatures_from_html(filename)

            # Extract full aetiology (Associated Aetiology)
            soup = BeautifulSoup(response.text, "html.parser")
            aetiology_td = soup.find("td", {"headers": "aet1"})
            associated_aetiology = aetiology_td.get_text(separator=" ", strip=True) if aetiology_td else "Unknown"

            print(f"{sbs} Aetiology: {aetiology}\n")
            print(f"{sbs} Second Aetiology: {associated_aetiology}\n")
            print(f"{sbs} Associated Signatures: {associated_signatures}\n")
        else:
            print(f"❌ Could not retrieve {sbs}. Status code: {response.status_code}")
        print("-" * 120)

    def run(self):
        """Runs the scraper for all SBS signatures."""
        for sbs in self.sbs_list:
            self.fetch_aetiology(sbs)


# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch SBS aetiologies and save HTML pages.")
    parser.add_argument("-l", "--list", required=True, help="Path to the text file containing SBS signatures (one per line).")
    args = parser.parse_args()

    scraper = SBSScraper(args.list)
    scraper.run()
