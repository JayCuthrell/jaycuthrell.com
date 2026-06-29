from pathlib import Path
import feedparser

# Setup paths relative to this script's location
src_dir = Path(__file__).parent
project_root = src_dir.parent
podcast_page_path = project_root / '_pages' / 'podcast.md'

def fetch_playlist_videos(playlist_id):
    """Fetches videos from a public YouTube playlist RSS feed."""
    rss_url = f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}"
    feed = feedparser.parse(rss_url)
    return feed.entries

if __name__ == "__main__":
    playlist_id = "PLbyE_u-MMuTvTa3AYInWSZwcDTw6nL-fR"
    videos = fetch_playlist_videos(playlist_id)
    
    # Define Jekyll Front Matter to ensure it maps to /podcast/
    # Using 'single' layout as defined in your defaults for a clean profile view
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
    video_list = []
    for video in videos:
        title = video.title
        link = video.link
        video_list.append(f" - [{title}]({link})")
        
    markdown_content = front_matter + "\n".join(video_list)
    
    # Write out to the _pages directory
    podcast_page_path.write_text(markdown_content, encoding="utf-8")
    print("Successfully updated podcast.md")