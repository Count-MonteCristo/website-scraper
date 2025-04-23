import pandas as pd
import csv
from .fetcher import fetch_html
from .parser import extract_info  # , extract_css_rules

def main():
    df = pd.read_csv('./data/input_urls.csv')
    urls = df['url'].dropna().tolist()
    results = []

    for url in urls:
        print(f"Processing: {url}")
        html = fetch_html(url)
        if html:
            info = extract_info(html, url)
            info['url'] = url
            results.append(info)

    if results:
        fieldnames = ['title', 'description', 'url', 'inline_style', 'h1_class', 'css_snippet']
        with open('./data/output.csv', 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(results)


if __name__ == "__main__":
    main()
