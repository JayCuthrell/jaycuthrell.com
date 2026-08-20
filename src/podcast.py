from pathlib import Path
import feedparser
import re

# Setup paths relative to this script's location
src_dir = Path(__file__).parent
project_root = src_dir.parent
podcast_page_path = project_root / '_pages' / 'podcast.md'

def fetch_podcast_episodes(rss_url):
    """Fetches episodes from the podcast RSS feed."""
    feed = feedparser.parse(rss_url)
    return feed.entries

def get_video_id(video_url):
    """Extracts the YouTube video ID from a URL."""
    match = re.search(r"v=([^&]+)", video_url)
    if match:
        return match.group(1)

if __name__ == "__main__":
    # Updated to use the new fudge.org podcast feed
    podcast_feed_url = "https://fudge.org/podcast.xml"
    episodes = fetch_podcast_episodes(podcast_feed_url)
    
    # Define Jekyll Front Matter to ensure it maps to /podcast/
    front_matter = (
        "---\n"
        "layout: post\n"
        "title: \"Podcast\"\n"
        "permalink: /podcast/\n"
        "author_profile: true\n"
        "---\n\n"
        "## Recent Episodes\n\n"
    )
    
    # Build markdown list items from entries
    episode_list = []
    for episode in episodes:
        title = episode.get('title', 'Unknown Episode')
        link = episode.get('link', '')
        description = episode.get('description', '')
        
        # Extract the MP3 audio URL from the feed's enclosure tag
        audio_url = ""
        if 'enclosures' in episode and len(episode.enclosures) > 0:
            audio_url = episode.enclosures[0].get('href', '')
        
        # Extract YouTube ID from the link tag
        video_id = get_video_id(link)
        
        # Build the HTML/Markdown output for the episode
        episode_html = f"### {title}\n\n"
        
        # Add an HTML5 Audio Player if the MP3 exists
        if audio_url:
            episode_html += (
                f'<audio controls style="width: 100%; margin-bottom: 15px;">\n'
                f'  <source src="{audio_url}" type="audio/mpeg">\n'
                f'  Your browser does not support the audio element.\n'
                f'</audio>\n\n'
            )
            
        # Add the YouTube embed if the video ID exists
        if video_id:
            episode_html += (
                f'<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto; margin-bottom: 15px;">\n'
                f'  <iframe src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>\n'
                f'</div>\n\n'
            )
            
        # Add the episode description
        if description:
            # Ensure the description is separated by blank lines so Markdown parses it correctly
            episode_html += f"{description}\n\n"
        
        episode_list.append(episode_html.strip())
        
    # Join episodes with a horizontal rule for clean visual separation
    markdown_content = front_matter + "\n\n<hr>\n\n".join(episode_list)
    
    # Write out to the _pages directory
    podcast_page_path.write_text(markdown_content, encoding="utf-8")
    print("Successfully updated podcast.md")