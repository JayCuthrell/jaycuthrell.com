from pathlib import Path
import datetime
import time
import feedparser
import pytz

# Setup robust file paths based on the location of this script
src_dir = Path(__file__).parent
project_root = src_dir.parent
newsletter_path = project_root / '_pages' / 'newsletter.md'
footer_path = project_root / 'FOOTER.md'

def update_footer():
    """Generates the footer with the current timestamp."""
    timestamp = datetime.datetime.now(pytz.timezone("America/New_York")).strftime("%c")
    footer = footer_path.read_text(encoding="utf-8")
    return footer.format(timestamp=timestamp)

def fetch_rss_entries(rss_feed_url):
    """Fetches and parses an RSS feed."""
    rss_feed = feedparser.parse(rss_feed_url)
    return rss_feed.entries

def combine_feeds(*feeds):
    """Combines any number of feeds and sorts them by publication date (newest first)."""
    combined_entries = []
    for feed in feeds:
        combined_entries.extend(feed)
    combined_entries.sort(key=lambda item: item.updated_parsed, reverse=True)
    return combined_entries

if __name__ == "__main__":
    rss_title = "### Recent Newsletter Issues by Jay Cuthrell on [fudge.org](https://fudge.org), [hot.fudge.org](https://hot.fudge.org), and [cuthrell.consulting](https://cuthrell.consulting)"
    newsletter_content = newsletter_path.read_text(encoding="utf-8")
    
    # Fetch and combine feeds
    feed1 = fetch_rss_entries("https://fudge.org/feed.xml")
    feed2 = fetch_rss_entries("https://hot.fudge.org/rss")
    feed3 = fetch_rss_entries("https://cuthrell.consulting/feed.xml")
    
    # Easily pass all three feeds into our new dynamic function
    combined_feed = combine_feeds(feed1, feed2, feed3)
    
    # Build the markdown list of posts
    posts = []
    for item in combined_feed:
        title = item.title
        link = item.link
        published = time.strftime('%Y %b %d', item.updated_parsed)
        posts.append(f" - [{title}]({link}) {published}")
    
    posts_joined = '\n'.join(posts)
    
    # Slice the old markdown and inject the new posts and updated footer
    updated_newsletter = newsletter_content[:newsletter_content.find(rss_title)] + f"{rss_title}\n{posts_joined}\n"
    
    with open(newsletter_path, "w", encoding="utf-8") as f:
        f.write(updated_newsletter + update_footer())