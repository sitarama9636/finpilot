import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tqdm import tqdm

def scrape_url_and_download_files(url: str, download_dir="downloads"):
    os.makedirs(download_dir, exist_ok=True)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch URL: {e}"}

    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text(separator=" ", strip=True)

    downloaded_files = []

    # Look for file links
    for link_tag in soup.find_all("a", href=True):
        href = link_tag['href']
        file_url = urljoin(url, href)
        if any(file_url.endswith(ext) for ext in [".pdf", ".docx", ".xlsx"]):
            try:
                filename = os.path.basename(urlparse(file_url).path)
                file_path = os.path.join(download_dir, filename)

                # Stream download with progress bar
                with requests.get(file_url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                downloaded_files.append(file_path)
            except Exception as err:
                print(f"Failed to download {file_url}: {err}")

    return {
        "text": page_text,
        "downloaded_files": downloaded_files
    }
