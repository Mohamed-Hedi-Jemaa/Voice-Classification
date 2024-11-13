import requests
import os
from bs4 import BeautifulSoup

# Function to get the URL for each participant
def url_num(number):
    return "http://stimmdb.coli.uni-saarland.de/details.php4?SprecherID=" + str(number)

url = 'http://stimmdb.coli.uni-saarland.de'

# Session initialization for requests
session = requests.Session()
session.post(url, data={'sb_search': 'Datenbankanfrage', 'sb_lang': 'English'})
session.post(url, data={'sb_sent': 'Accept', 'n': '1'})

# Ensure directory exists
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Main function to download dataset
def download_dataset():
    # 2741 is the ID number of the last participant
    for i in range(0, 2742):
        session = requests.Session()
        session.post(url, data={'sb_search': 'Datenbankanfrage', 'sb_lang': 'English'})
        session.post(url, data={'sb_sent': 'Accept'})

        # Fetch participant data and check response status
        response = session.get(url_num(i))
        print(f"Connection Status for ID {i}: {response.status_code}")
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Determine gender
        for gender in soup.find('div', attrs={'class', 'title'}):
            if 'female' in gender:
                gend = "female"
            else:
                gend = "male"
        print(f"ID: {i}, Gender: {gend}")

        # Process each session
        for group in soup.findAll('table', attrs={'class', 'sessiondetails'}):
            for t in group.findAll('td', {'class': 'detailstd', 'colspan': '2'}):
                if t.text.startswith('healthy'):
                    # Set directory and ensure it exists
                    path = "dataset/healthy/" + gend
                    ensure_dir(path)
                    
                    # Download each file link
                    for link in group.findAll('a', attrs={'target': 'PLAY'}):
                        file_link = "http://stimmdb.coli.uni-saarland.de/" + link.get('href')
                        file_name = str(i) + "_" + file_link[54:]
                        file_path = os.path.join(path, file_name + ".wav")

                        # Download file and check status
                        doc = requests.get(file_link)
                        if doc.status_code == 200:
                            with open(file_path, 'wb') as f:
                                f.write(doc.content)
                            print(f"Saved: {file_path}")
                        else:
                            print(f"Failed to download {file_link} with status {doc.status_code}")
                    break

                elif t.text.startswith('pathological'):
                    # Set directory and ensure it exists
                    path = "dataset/pathological/" + gend
                    ensure_dir(path)
                    
                    # Download each file link
                    for link in group.findAll('a', attrs={'target': 'PLAY'}):
                        file_link = "http://stimmdb.coli.uni-saarland.de/" + link.get('href')
                        file_name = str(i) + "_" + file_link[54:]
                        file_path = os.path.join(path, file_name + ".wav")

                        # Download file and check status
                        doc = requests.get(file_link)
                        if doc.status_code == 200:
                            with open(file_path, 'wb') as f:
                                f.write(doc.content)
                            print(f"Saved: {file_path}")
                        else:
                            print(f"Failed to download {file_link} with status {doc.status_code}")
                    break

        print(f"Data for User {i} is processed.\n")

# Run the dataset download function
download_dataset()
