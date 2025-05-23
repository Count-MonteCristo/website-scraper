from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from PIL import Image
Image.MAX_IMAGE_PIXELS = 250_000_000
from io import BytesIO
import requests
from .default_html import (
    default_html_student_v1,
    default_html_student_v2,
    default_html_employer_v1,
    default_html_employer_v2,
    default_featured_projects_html
)

def rgb_to_hex(rgb):
    """Convert an RGB tuple to a HEX color."""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def normalize_html(html):
    """Normalize HTML by parsing and re-serializing it to ensure consistent formatting."""
    return ''.join(BeautifulSoup(html, 'html.parser').stripped_strings)

def extract_info(html, url, page_type='employer'):
    soup = BeautifulSoup(html, 'html.parser')

    # Extract intro text from the page
    intro_text = ''
    intro_section = soup.find('div', class_='two-columns-content-section')

    # Fallback to class='banner-content' if class='two-columns-content-section' is not found
    if not intro_section:
        intro_section = soup.find('div', class_='banner-content')

    if intro_section:
        # Get all <p> elements and filter out those with only whitespace or non-breaking spaces
        paragraphs = intro_section.find_all('p')
        valid_paragraphs = [
            p for p in paragraphs if p.get_text(strip=True)  # Only include <p> elements with actual text
        ]
        # Concatenate the HTML content of valid <p> elements
        intro_text = ''.join(str(p) for p in valid_paragraphs)

    # Compare intro text with default variations based on page type
    intro_text_differs = "Yes"  # Default to "Yes"

    # Normalize both the extracted intro_text and the default HTML templates
    normalized_intro_text = normalize_html(intro_text)
    normalized_default_html_employer_v2 = normalize_html(default_html_employer_v2)

    if page_type == 'student' and (
        normalized_intro_text == normalize_html(default_html_student_v1) or
        normalized_intro_text == normalize_html(default_html_student_v2)
    ):
        intro_text = ''  # Leave empty if it matches either default variation
        intro_text_differs = "No"  # Set to "No" if it matches a default variation
    elif page_type == 'employer' and (
        normalized_intro_text == normalize_html(default_html_employer_v1) or
        normalized_intro_text == normalized_default_html_employer_v2
    ):
        intro_text = ''  # Leave empty if it matches either default variation
        intro_text_differs = "No"  # Set to "No" if it matches a default variation

    # Extract hs_name from the title
    title = soup.title.string.strip() if soup.title else ''
    hs_name = ''
    
    if title:
        match = re.search(
            r"(?:Micro-Internships For On-Demand Project Support from|Micro-Internships for|Recruit|The|Support|^(.+?) Micro-Internships) (?:students and recent grads of )?(?:from )?(.+?)(?: Scholars| (students|Student-Athletes|graduates|grads|Alumni with Micro-Internships|with Micro-Internships|Micro-Internship Program)|,|$)",
            title,
            re.IGNORECASE
        )
        if match:
            hs_name = match.group(1).strip() if match.group(1) else match.group(2).strip()

    # Extract hs_path from the URL
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) > 1 and path_parts[0] in ['employer', 'student']:
        hs_path = path_parts[1]
    else:
        hs_path = path_parts[0]

    # Extract partner_logo and measure its dimensions using Pillow
    partner_logo = ''
    partner_logo_width = ''
    partner_logo_height = ''
    partner_logo_orientation = ''
    partner_logo_url = ''
    img_tag = soup.find('img', class_='hs-image-widget')
    
    if img_tag and img_tag.get('src'):
        partner_logo = img_tag['src']
        try:
            # Download the image and measure its dimensions
            response = requests.get(partner_logo, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            partner_logo_width, partner_logo_height = img.size
            # Determine orientation
            if partner_logo_width > partner_logo_height:
                partner_logo_orientation = 'horizontal'
            elif partner_logo_width < partner_logo_height:
                partner_logo_orientation = 'vertical'
            else:
                partner_logo_orientation = 'square'
        except Exception as e:
            print(f"Error measuring image dimensions: {e}")

    # Extract partner_logo_url from the <a> tag wrapping the <img> tag
    if img_tag:
        parent_a_tag = img_tag.find_parent('a')
        if parent_a_tag and parent_a_tag.get('href'):
            partner_logo_url = parent_a_tag['href']
            # Normalize protocol-relative URLs
            if partner_logo_url.startswith("//"):
                partner_logo_url = "https:" + partner_logo_url
        else:
            # If the <a> tag exists but has no href, set to "N/A"
            partner_logo_url = "N/A"

    # Extract featured_image from the <meta> tag with property="og:image"
    featured_image = 'N/A'
    meta_tag = soup.find('meta', property='og:image')
    if meta_tag and meta_tag.get('content'):
        featured_image = meta_tag.get('content')

    # Extract featured projects section only for employer pages
    standard_featured_project_list_differs = "N/A"  # Default to N/A
    if page_type == 'employer':
        featured_projects_section = soup.find('div', class_='features-box-row')
        featured_projects_html = str(featured_projects_section) if featured_projects_section else ''

        if featured_projects_html:  # Only compare if the section exists
            normalized_featured_projects_html = normalize_html(featured_projects_html)
            normalized_default_featured_projects_html = normalize_html(default_featured_projects_html)

            if normalized_featured_projects_html == normalized_default_featured_projects_html:
                standard_featured_project_list_differs = "No"
            else:
                standard_featured_project_list_differs = "Yes"

    # Use Selenium to extract the secondary color
    secondary_color = ''
    primary_color = ''
    try:
        options = Options()
        options.add_argument('--headless')  # Run in headless mode
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        try:
            # Locate the button with the "question" class and extract the border color
            try:
                question_button = driver.find_element(By.CLASS_NAME, 'question')
                border_color = driver.execute_script(
                    "return window.getComputedStyle(arguments[0]).getPropertyValue('border-left-color');",
                    question_button
                )
                match = re.search(r'rgb\((\d+), (\d+), (\d+)\)', border_color)
                if match:
                    rgb = tuple(map(int, match.groups()))
                    secondary_color = rgb_to_hex(rgb)
                    print(f"[INFO] Extracted secondary color from button border: {secondary_color}")
            except Exception:
                print("[INFO] 'question' button not found, checking 'cta_button'.")

            # Fallback to the background color of the "cta_button" class
            if not secondary_color:
                try:
                    cta_button = driver.find_element(By.CLASS_NAME, 'cta_button')
                    background_color = driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).getPropertyValue('background-color');",
                        cta_button
                    )
                    match = re.search(r'rgb\((\d+), (\d+), (\d+)\)', background_color)
                    if match:
                        rgb = tuple(map(int, match.groups()))
                        secondary_color = rgb_to_hex(rgb)
                        print(f"[INFO] Extracted secondary color from cta_button background: {secondary_color}")
                except Exception:
                    print("[INFO] 'cta_button' not found, checking 'hs-button'.")

            # Fallback to the background color of the "hs-button" class
            if not secondary_color:
                try:
                    hs_button = driver.find_element(By.CLASS_NAME, 'hs-button')
                    background_color = driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).getPropertyValue('background-color');",
                        hs_button
                    )
                    match = re.search(r'rgb\((\d+), (\d+), (\d+)\)', background_color)
                    if match:
                        rgb = tuple(map(int, match.groups()))
                        secondary_color = rgb_to_hex(rgb)
                        print(f"[INFO] Extracted secondary color from hs-button background: {secondary_color}")
                except Exception as e:
                    print(f"[INFO] 'hs-button' not found or error extracting color: {e}")
                    secondary_color = "N/A"  # Return N/A if no secondary color is found
        except Exception as e:
            print(f"Error extracting secondary color: {e}")
            secondary_color = "N/A"  # Return N/A if an unexpected error occurs

        # Extract the primary color after defining the secondary color
        # Locate the target element for primary color
        try:
            banner_section = driver.find_element(By.CLASS_NAME, 'hnh-content')
            background_image = driver.execute_script(
                "return window.getComputedStyle(arguments[0]).getPropertyValue('background-image');",
                banner_section
            )
            match = re.search(r'rgb\((\d+), (\d+), (\d+)\)', background_image)
            if match:
                rgb = tuple(map(int, match.groups()))
                primary_color = rgb_to_hex(rgb)
                print(f"[INFO] Extracted primary color from .hnh-content: {primary_color}")
        except Exception:
            print("[INFO] .hnh-content not found, checking .banner-section")

        # Fallback to .banner-section if .hnh-content is not found
        if not primary_color:
            try:
                banner_section = driver.find_element(By.CLASS_NAME, 'banner-section')
                background_image = driver.execute_script(
                    "return window.getComputedStyle(arguments[0]).getPropertyValue('background-image');",
                    banner_section
                )
                match = re.search(r'rgb\((\d+), (\d+), (\d+)\)', background_image)
                if match:
                    rgb = tuple(map(int, match.groups()))
                    primary_color = rgb_to_hex(rgb)
                    print(f"[INFO] Extracted primary color from .banner-section: {primary_color}")
            except Exception:
                print("[INFO] .banner-section not found, checking .qicon")

        # Fallback to .qicon if .banner-section is not found
        if not primary_color:
            try:
                qicon_element = driver.find_element(By.CLASS_NAME, 'qicon')
                background_color = driver.execute_script(
                    "return window.getComputedStyle(arguments[0]).getPropertyValue('background');",
                    qicon_element
                )
                match = re.search(r'rgba?\((\d+), (\d+), (\d+)', background_color)
                if match:
                    rgb = tuple(map(int, match.groups()))
                    hex_color = rgb_to_hex(rgb)
                    if hex_color in ['#ffffff', '#cccccc']:  # Check if the color is white or grey
                        primary_color = secondary_color  # Use secondary color as fallback
                        print("[INFO] Fallback to secondary color as primary color is white or grey.")
                    else:
                        primary_color = hex_color
                        print(f"[INFO] Extracted primary color from .qicon: {primary_color}")
            except Exception as e:
                print(f"[INFO] .qicon not found or error extracting color: {e}")

        # Ensure primary color is set if it's empty but secondary color is available
        if not primary_color and secondary_color:
            primary_color = secondary_color
            print("[INFO] Fallback to secondary color for primary color as primary color is empty.")

        driver.quit()
    except Exception as e:
        print(f"Error extracting colors: {e}")

    return {
        'hs_name': hs_name,
        'hs_path': hs_path,
        'partner_logo': partner_logo,
        'partner_logo_width': partner_logo_width,
        'partner_logo_height': partner_logo_height,
        'partner_logo_orientation': partner_logo_orientation,
        'partner_logo_url': partner_logo_url,
        'primary_color': primary_color,
        'secondary_color': secondary_color,
        'featured_image': featured_image,
        'intro_text': intro_text,
        'intro_text_differs': intro_text_differs,
        'standard_featured_project_list_differs': standard_featured_project_list_differs
    }
