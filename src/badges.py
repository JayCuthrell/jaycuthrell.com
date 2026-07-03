from pathlib import Path
import json
import urllib.request

# Setup paths relative to this script's location
src_dir = Path(__file__).parent
project_root = src_dir.parent
badges_page_path = project_root / '_pages' / 'badges.md'

def fetch_credly_badges(username):
    """Fetches badges from the public Credly user JSON endpoint."""
    url = f"https://www.credly.com/users/{username}/badges.json"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (compatible; JayCuthrellSiteBot/1.0)'}
    )
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
    return data.get('data', [])

if __name__ == "__main__":
    username = "jaycuthrell"
    badges = fetch_credly_badges(username)
    
    # Define Jekyll Front Matter matching your site defaults
    front_matter = (
        "---\n"
        "layout: post\n"
        "title: \"Certifications & Badges\"\n"
        "permalink: /badges/\n"
        "author_profile: true\n"
        "---\n\n"
        "## Verified Credly Badges\n\n"
    )
    
    # Build markdown image links for each badge
    badge_list = []
    for item in badges:
        template = item.get('badge_template', {})
        badge_name = template.get('name', 'Badge')
        image_url = template.get('image', {}).get('url', '')
        badge_id = item.get('id')
        badge_url = f"https://www.credly.com/badges/{badge_id}"
        
        if image_url and badge_url:
            # Renders as a linked badge image pointing to the Credly verification page
            badge_list.append(
                f'<a href="{badge_url}" target="_blank" title="{badge_name}">'
                f'<img src="{image_url}" alt="{badge_name}" width="150" style="margin: 10px; display: inline-block;" />'
                f'</a>'
            )
        
    markdown_content = front_matter + "<div style=\"text-align: center;\">\n" + "\n".join(badge_list) + "\n</div>\n"
    
    # Write out to the _pages directory
    badges_page_path.write_text(markdown_content, encoding="utf-8")
    print("Successfully updated badges.md")