# 🕸️ Local Web Scraper

A lightweight Python-based web scraper designed to extract specific data from a list of URLs. The scraper fetches HTML content, parses it, and extracts key information such as colors, images, and metadata. Results are saved to a CSV file for easy analysis.

## 📋 Features

- **Input from CSV**: Reads a list of URLs from `data/input_urls.csv`.
- **HTML Fetching**: Uses `requests` to fetch HTML content.
- **Data Extraction**: Extracts:
  - Primary and secondary colors from CSS styles.
  - Partner logos and their dimensions.
  - Metadata such as featured images and page titles.
- **Fallback Logic**: Handles missing elements with multiple fallback strategies.
- **Output to CSV**: Saves extracted data to `data/output.csv`.
- **Error Handling**: Logs failed URLs for review.

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Google Chrome installed
- ChromeDriver installed and added to your PATH

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Count-MonteCristo/website-scraper.git
   cd web-scraper-local
   ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Verify ChromeDriver installation:
    ```bash
    chromedriver --version
    ```

## 📂 Project Structure

```bash
web-scraper-local/
├── data/
│   ├── input_urls.csv      # Input file containing URLs to scrape
│   ├── output.csv          # Output file with extracted data
├── scraper/
│   ├── fetcher.py          # Handles HTML fetching
│   ├── parser.py           # Extracts data from HTML
│   ├── main.py             # Main script to run the scraper
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 🚀 Usage

1. Add URLs to `data/input_urls.csv`
   ```bash
    url
    https://example.com/page1
    https://example.com/page2
   ```
2. Run the scraper\
    Execute the following command:
    ```bash
    python -m scraper.main
    ```

3. View the results\
The extracted data will be saved to `data/output.csv` in the following format:
    ```bash
    hs_name,hs_path,partner_logo,partner_logo_width,partner_logo_height,partner_logo_orientation,partner_logo_url,primary_color,secondary_color,featured_image,url
    ExampleUniversity,example,https://example.com/logo.png,300,150,horizontal,https://example.com,#ff5733,#33aaff,https://example.com/featured.png,https://example.com
    ```

## 🧩 How It Works

1. Fetch HTML\
    The scraper uses the `requests` library to fetch HTML content from the provided URLs.

2. Parse HTML\
    The `BeautifulSoup` library is used to parse the HTML and locate specific elements.

3. Extract Data\
    The scraper extracts:
    - Primary Color: Extracted from gradients or background colors of specific elements.
    - Secondary Color: Extracted from border or background colors of fallback elements.
    - Partner Logo: Extracted from `<img>` tags, including dimensions and orientation.
    - Featured Image: Extracted from `<meta>` tags with `og:image`.

4. Fallback Logic\
    If a primary or secondary color is not found, the scraper uses fallback elements or defaults to `N/A`.

## 🛠️ Configuration

### ChromeDriver
Ensure that ChromeDriver is installed and matches your version of Google Chrome. You can download it from [ChromeDriver Downloads](https://developer.chrome.com/docs/chromedriver).

## 🐞 Error Handling

- **Failed URLs**: If a URL fails to fetch or parse, it will be logged in the terminal output.
- **Missing Data**: If specific elements are not found, the scraper will use fallback logic or return `N/A`.

## 🧪 Testing

To test the scraper:\

1. Add test URLs to `data/input_urls.csv`.

2. Run the scraper:\
    ```bash
    python -m scraper.main
    ```

3. Verify the output in `data/output.csv`.

## 📦 Dependencies

The project uses the following Python libraries:\

- `beautifulsoup4`: HTML parsing
- `requests`: HTTP requests
- `selenium`: Browser automation for CSS extraction
- `pillow`: Image processing
- `pandas`: CSV handling
- `tqdm`: Progress bars
- `colorama`: Colored terminal output

Install all dependencies with:\
```bash
pip install -r requirements.txt
```

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙋‍♂️ FAQ

1. What happens if a URL fails to load?\
The scraper logs the failed URL and continues processing the remaining URLs.

2. How do I update ChromeDriver?\
Download the latest version from [ChromeDriver Downloads](https://developer.chrome.com/docs/chromedriver) and replace the existing binary.

3. Can I add custom extraction logic?\
Yes! Modify the `parser.py` file to include additional logic for extracting data.
