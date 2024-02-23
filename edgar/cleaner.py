from bs4 import BeautifulSoup
import html
import os
import pandas as pd
import re
from collections import Counter


# =====================================================================
# clean_html_files
# =====================================================================

def is_10k_html(file_name: str) -> bool:
    if file_name.endswith('.html') or file_name.endswith('.htm'):
        return True
    return False

# Take in an html text string. Return the cleaned text
def clean_html_text(html_text: str) -> str:
    soup = BeautifulSoup(html_text, 'html.parser')
    clean_text = soup.get_text(separator=' ', strip=True)
    return clean_text


# Write all html 10-k files in the input folder into the destination
# folder as cleaned txt files.
# Naming convention: <ticker>_10-k_<filing_date>.json
def write_clean_html_json_files(input_folder: str, 
                                dest_folder: str) -> None:
    input_names = os.listdir(input_folder)
    input_paths = [os.path.join(input_folder, name) for name in input_names]
    inputs = {name: path for name, path in zip(input_names, input_paths) if is_10k_html(path)}

    cleaned = {}
    
    for name, path in inputs.items():
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            cleaned[name] = clean_html_text(content)

    for name, text in cleaned.items():
        dest_path = os.path.join(dest_folder, name)
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(text)

    print(f"write_clean_html_text_files(): {len(cleaned)} files cleaned")
