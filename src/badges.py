from pathlib import Path
import json
import urllib.request

# Setup paths relative to this script's location
src_dir = Path(__file__).parent
project_root = src_dir.parent
badges_page_path = project_root / '_pages' / 'badges.md'

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

def generate_unified_badges_page(badges):
    """Generates a single _pages/badges.md file containing both badges and skills."""
    # 1. Process Badges Gallery
    badge_list = []
    unique_skills = set()
    
    for item in badges:
        template = item.get('badge_template', {})
        badge_name = template.get('name', 'Badge')
        image_url = template.get('image', {}).get('url', '')
        badge_id = item.get('id')
        badge_url = f"https://www.credly.com/badges/{badge_id}"
        
        # Build badge image link
        if image_url and badge_url:
            badge_list.append(
                f'<a href="{badge_url}" target="_blank" title="{badge_name}">'
                f'<img src="{image_url}" alt="{badge_name}" width="140" style="margin: 10px; display: inline-block;" />'
                f'</a>'
            )
            
        # Extract skills tied to this badge
        skills = template.get('skills', [])
        for skill in skills:
            if 'name' in skill:
                unique_skills.add(skill['name'])
                
    sorted_skills = sorted(list(unique_skills))
    
    # 2. Build Front Matter
    front_matter = (
        "---\n"
        "layout: post\n"
        "title: \"Certifications & Skills\"\n"
        "permalink: /badges/\n"
        "author_profile: true\n"
        "---\n\n"
    )
    
    # 3. Assemble Markdown Content
    badges_section = (
        "## Verified Certifications & Badges\n\n"
        '<div style="text-align: center;">\n' + "\n".join(badge_list) + "\n</div>\n\n"
    )
    
    skills_section = (
        "## Verified Skills Wallet\n\n"
        "These skills have been independently verified and backed by my earned Credly certifications above.\n\n"
        + "\n".join([f"* **{skill}**" for skill in sorted_skills]) + "\n"
    )
    
    # Write combined output to _pages/badges.md
    full_content = front_matter + badges_section + "---\n\n" + skills_section
    badges_page_path.write_text(full_content, encoding="utf-8")
    print(f"Successfully updated badges.md with {len(badge_list)} badges and {len(sorted_skills)} verified skills.")

if __name__ == "__main__":
    username = "jaycuthrell"
    print(f"Fetching Credly data for {username}...")
    badge_data = fetch_credly_data(username)
    
    if badge_data:
        generate_unified_badges_page(badge_data)
    else:
        print("No badge data found or error fetching data.")