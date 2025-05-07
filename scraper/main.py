import pandas as pd
import csv
from tqdm import tqdm
from colorama import Fore, Style, init
from .fetcher import fetch_html
from .parser import extract_info

# Initialize colorama
init(autoreset=True)

def main():
    df = pd.read_csv('./data/input_urls.csv')
    urls = df['url'].dropna().tolist()
    results = []
    failed_urls = []

    tqdm.write(f"{Fore.CYAN}Starting the scraping process for {len(urls)} URLs...\n")

    fieldnames = [
        'hs_name', 'hs_path', 'partner_logo', 'partner_logo_width',
        'partner_logo_height', 'partner_logo_orientation', 'partner_logo_url',
        'primary_color', 'secondary_color', 'featured_image',
        'intro_text_differs', 'intro_text', 'url'
    ]

    with tqdm(total=len(urls), desc="Scraping Progress", unit="url", dynamic_ncols=True) as pbar:
        for url in urls:
            tqdm.write(f"\n{Fore.BLUE}[INFO] Starting processing for URL: {url}")
            
            tqdm.write(f"{Fore.BLUE}[INFO] Fetching HTML for URL: {url}")
            html = fetch_html(url)
            if html and not html.startswith("HTTPError") and not html.startswith("Invalid URL"):
                tqdm.write(f"{Fore.GREEN}[INFO] Successfully fetched HTML for URL: {url}")
                
                tqdm.write(f"{Fore.BLUE}[INFO] Extracting information from URL: {url}")
                try:
                    info = extract_info(html, url)
                    info['url'] = url  # Add the URL to the extracted info
                    results.append(info)
                    tqdm.write(f"{Fore.GREEN}[INFO] Successfully extracted information for URL: {url}")
                except Exception as e:
                    tqdm.write(f"{Fore.RED}[ERROR] Failed to extract information for URL: {url}: {e}")
                    failed_urls.append((url, f"Extraction error: {e}"))
            else:
                tqdm.write(f"{Fore.RED}[ERROR] Failed to fetch HTML for URL: {url}: {html}")
                failed_urls.append((url, html))
            
            pbar.set_postfix_str(f"Processing: {url}")
            pbar.update(1)

    if results:
        tqdm.write(f"\n{Fore.CYAN}[INFO] Writing results to './data/output.csv'...")
        with open('./data/output.csv', 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(results)
        tqdm.write(f"{Fore.GREEN}[INFO] Results successfully written to './data/output.csv'.")
    else:
        tqdm.write(f"\n{Fore.YELLOW}[WARNING] No results to save. Please check the input URLs or the scraper logic.")

    if failed_urls:
        tqdm.write(f"\n{Fore.YELLOW}[WARNING] The following URLs failed during the scraping process:")
        for url, reason in failed_urls:
            tqdm.write(f"  {Fore.RED}- {url}: {reason}")
        tqdm.write(f"\n{Fore.CYAN}[INFO] Please review the failed URLs and try again if necessary.")
    else:
        tqdm.write(f"\n{Fore.GREEN}[INFO] All URLs processed successfully!")

if __name__ == "__main__":
    main()
