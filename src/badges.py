from pathlib import Path
import json
import urllib.request

# Setup paths relative to this script's location
src_dir = Path(__file__).parent
project_root = src_dir.parent
badges_page_path = project_root / '_pages' / 'badges.md'
skills_page_path = project_root / '_pages' / 'skills.md'

def fetch_credly_data(username):
    """Fetches badge and skill data from the public Credly user JSON endpoint."""
    url = f"https://www.credly.com/users/{username}/badges.json"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (compatible; JayCuthrellSiteBot/1.0)'}
    )
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
    return data.get('data', [])

def generate_badges_page(badges):
    """Generates the _pages/badges.md markdown file."""
    front_matter = (
        "---\n"
        "layout: post\n"
        "title: \"Certifications & Badges\"\n"
        "permalink: /badges/\n"
        "author_profile: true\n"
        "---\n\n"
        "## Verified Credly Badges\n\n"
    )
    
    badge_list = []
    for item in badges:
        template = item.get('badge_template', {})
        badge_name = template.get('name', 'Badge')
        image_url = template.get('image', {}).get('url', '')
        badge_id = item.get('id')
        badge_url = f"https://www.credly.com/badges/{badge_id}"
        
        if image_url and badge_url:
            badge_list.append(
                f'<a href="{badge_url}" target="_blank" title="{badge_name}">'
                f'<img src="{image_url}" alt="{badge_name}" width="150" style="margin: 10px; display: inline-block;" />'
                f'</a>'
            )
            
    markdown_content = front_matter + '<div style="text-align: center;">\n' + "\n".join(badge_list) + "\n</div>\n"
    badges_page_path.write_text(markdown_content, encoding="utf-8")
    print("Successfully updated badges.md")

def generate_skills_page(badges):
    """Extracts unique skills from badge templates and generates _pages/skills.md."""
    unique_skills = set()
    for item in badges:
        template = item.get('badge_template', {})
        skills = template.get('skills', [])
        for skill in skills:
            if 'name' in skill:
                unique_skills.add(skill['name'])
                
    sorted_skills = sorted(list(unique_skills))
    
    front_matter = (
        "---\n"
        "layout: page\n"
        "title: \"Verified Skills Wallet\"\n"
        "permalink: /skills/\n"
        "author_profile: true\n"
        "---\n\n"
        "These skills have been independently verified and backed by my earned "
        "[Credly certifications](/badges/).\n\n"
    )
    
    skill_list = [f"* **{skill}**" for skill in sorted_skills]
    markdown_content = front_matter + "\n".join(skill_list) + "\n"
    skills_page_path.write_text(markdown_content, encoding="utf-8")
    print(f"Successfully updated skills.md ({len(sorted_skills)} verified skills)")

if __name__ == "__main__":
    username = "jaycuthrell"
    print(f"Fetching Credly data for {username}...")
    badge_data = fetch_credly_data(username)
    
    if badge_data:
        generate_badges_page(badge_data)
        generate_skills_page(badge_data)
    else:
        print("No badge data found or error fetching data.")