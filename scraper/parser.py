from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
import requests

def extract_info(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    
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

    return {
        'hs_name': hs_name,
        'hs_path': hs_path,
        'partner_logo': partner_logo,
        'partner_logo_width': partner_logo_width,
        'partner_logo_height': partner_logo_height,
        'partner_logo_orientation': partner_logo_orientation,
        'partner_logo_url': partner_logo_url,
        'primary_color': '',  # Placeholder
        'secondary_color': '',  # Placeholder
        'featured_image': ''  # Placeholder
    }
