import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO


def get_file(filename: str,
             url: str,
             write_as: str = "wb",
             show_results: bool = True
             ) -> None:

    response = requests.get(url)

    response.raise_for_status()

    with open(filename, write_as) as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    if show_results == True:
        print("Download complete.")

def html_table_by_id(
        url: str,
        table_id: str,
        index: int = 0,
        show_results: bool = True
        ) -> pd.DataFrame:
    
    # This 'User-Agent' tells the website you are a standard Windows Chrome browser.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    # Scrape the page
    response = requests.get(url, headers = headers)

    # Check if scrape was successful
    response.raise_for_status()

    # Convert HTML code into structured data
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find table based on ID
    target_table = soup.find_all('table', {'id': table_id})
    
    if target_table:
        if index >= len(target_table):
            print("Index out of range.")
            return pd.DataFrame()
        
        # Convert back to string and tell Pandas to not look for a file
        df = pd.read_html(StringIO(str(target_table[index])))[0]
        
        if show_results == True:
            print(df.head())
        return df

    else:
        print("Table ID not found.")
    
    return pd.DataFrame()

def html_table_by_headers(
    url: str,
    table_headers: list[str],
    index: int = 0,
    show_results: bool = True
) -> pd.DataFrame:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")

    normalized_target = {h.lower().strip() for h in table_headers}

    matches = []

    for table in tables:
        ths = table.find_all("th")
        html_headers = {th.get_text(strip=True).lower() for th in ths}

        if normalized_target.issubset(html_headers):
            matches.append(table)

    if not matches:
        print("No matching table found.")
        return pd.DataFrame()

    if index >= len(matches):
        print(f"Index {index} out of range. Found {len(matches)} matching table(s).")
        return pd.DataFrame()

    df = pd.read_html(StringIO(str(matches[index])))[0]

    if show_results:
        print(df.head())

    return df