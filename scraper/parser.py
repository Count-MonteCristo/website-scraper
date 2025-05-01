from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

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
        hs_path = path_parts[1]  # Use the second part for cases like /employer/cuw
    else:
        hs_path = path_parts[0]  # Use the first part for cases like /csun or /csun/featured

    return {
        'hs_name': hs_name,
        'hs_path': hs_path,
        'partner_logo': '',  # Placeholder
        'partner_logo_width': '',  # Placeholder
        'partner_logo_height': '',  # Placeholder
        'partner_logo_orientation': '',  # Placeholder
        'partner_logo_url': '',  # Placeholder
        'primary_color': '',  # Placeholder
        'secondary_color': '',  # Placeholder
        'featured_image': ''  # Placeholder
    }
