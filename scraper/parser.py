from bs4 import BeautifulSoup
import tinycss2

def extract_info(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract title and meta description
    title = soup.title.string.strip() if soup.title else ''
    description = ''
    if desc := soup.find('meta', attrs={'name': 'description'}):
        description = desc.get('content', '').strip()

    # Example: extract inline style from the first <div>
    first_div = soup.find('div')
    inline_style = first_div.get('style', '') if first_div else ''

    # Example: extract class from an h1
    first_h1 = soup.find('h1')
    h1_class = ' '.join(first_h1.get('class', [])) if first_h1 else ''

    # Extract and parse <style> tag CSS rules
    styles = []
    for style_tag in soup.find_all("style"):
        rules = tinycss2.parse_stylesheet(style_tag.string or "", skip_comments=True, skip_whitespace=True)
        for rule in rules:
            if rule.type == 'qualified-rule':
                selector = ''.join([x.serialize() for x in rule.prelude]).strip()
                declarations = ''.join([x.serialize() for x in rule.content]).strip()
                styles.append(f"{selector} {{ {declarations} }}")

    css_summary = '; '.join(styles[:3])  # just a short sample of the rules

    return {
        'title': title,
        'description': description,
        'url': url,
        'inline_style': inline_style,
        'h1_class': h1_class,
        'css_snippet': css_summary
    }
