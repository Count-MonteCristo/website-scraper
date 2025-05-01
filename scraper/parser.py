from bs4 import BeautifulSoup
import re

def extract_info(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract the title
    title = soup.title.string.strip() if soup.title else ''
    
    # Extract hs_name from the title
    hs_name = ''
    if title:
        # Match patterns like:
        # "Micro-Internships for [Name]"
        # "Recruit [Name] students with Micro-Internships"
        # "Micro-Internships for students and recent grads of [Name]"
        # "Micro-Internships for [Name], [Additional Info]"
        # "The [Name] Micro-Internship Program"
        # "Support [Name] Alumni with Micro-Internships"
        # "Micro-Internships For On-Demand Project Support from [Name] Scholars"
        # "[Name] Micro-Internships | Optimize Early-Career Hiring With Parker Dewey"
        match = re.search(
            r"(?:Micro-Internships For On-Demand Project Support from|Micro-Internships for|Recruit|The|Support|^(.+?) Micro-Internships) (?:students and recent grads of )?(?:from )?(.+?)(?: Scholars| (students|Student-Athletes|graduates|grads|Alumni with Micro-Internships|with Micro-Internships|Micro-Internship Program)|,|$)",
            title,
            re.IGNORECASE
        )
        if match:
            # Check if the first group captures the institution name
            hs_name = match.group(1).strip() if match.group(1) else match.group(2).strip()

    return {
        'hs_name': hs_name,
        'hs_path': '',  # Placeholder
        'partner_logo': '',  # Placeholder
        'partner_logo_width': '',  # Placeholder
        'partner_logo_height': '',  # Placeholder
        'partner_logo_orientation': '',  # Placeholder
        'partner_logo_url': '',  # Placeholder
        'primary_color': '',  # Placeholder
        'secondary_color': '',  # Placeholder
        'featured_image': ''  # Placeholder
    }
