#!/usr/bin/env python3
"""Download remaining vocabulary pages 13-39"""

import requests
import time
import os
from pathlib import Path

def download_page(url, page_num):
    """Download a single page and save to file"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    }

    try:
        print(f"Downloading page {page_num}...", end=" ", flush=True)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Remove HTML tags
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text('\n')

        # Save to file
        filename = f"data/{page_num}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)

        lines = len(text.split('\n'))
        print(f"✓ {lines} lines saved")
        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Read links from links.md
links = []
with open('links.md', 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('{'):  # Skip header
            continue
        if '[' in line and '](http' in line:
            # Extract URL from markdown link format [text](url)
            start = line.find('](') + 2
            end = line.find(')', start)
            if start > 1 and end > start:
                url = line[start:end]
                links.append(url)

print(f"Found {len(links)} total links")

# Re-download page 13 only
for i in range(12, 13):  # Index 12 = page 13
    page_num = i + 1
    url = links[i]

    # Force re-download by removing skip check
    filepath = f"data/{page_num}.txt"
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Removed existing {filepath}")

    success = download_page(url, page_num)
    if success:
        time.sleep(1)  # Be respectful
    else:
        print(f"Failed to download page {page_num}")
        time.sleep(2)

print("Download complete!")
