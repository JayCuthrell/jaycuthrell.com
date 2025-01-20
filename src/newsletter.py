from pathlib import Path
import datetime
import time
import feedparser
import pytz

def update_footer():
    timestamp = datetime.datetime.now(pytz.timezone("America/New_York")).strftime("%c")
    footer = Path('../FOOTER.md').read_text()
    return footer.format(timestamp=timestamp)

def reverse_rss_feed(rss_feed_url):
    rss_feed = feedparser.parse(rss_feed_url)
    # new format as of Eleventy Excellent 3.7.3
    # rss_feed.entries.reverse()
    return rss_feed.entries

def update_readme_buttondown_posts(buttondown_feed, readme_base, join_on):
    rss_feed_url = buttondown_feed
    rss_feed_entries = reverse_rss_feed(rss_feed_url)
    posts = []
    for item in rss_feed_entries:
        # Accessing tags directly using the namespace
        title = item.title
        link = item.link
        published = (time.strftime('%Y %b %d', item.updated_parsed))  # Using updated_parsed
        posts.append(f" - [{title}]({link}) {published}")
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title)] + f"{join_on}\n{posts_joined}"

def combine_feeds(feed1, feed2, feed3):
    combined_entries = feed1 + feed2 + feed3
    combined_entries.sort(key=lambda item: item.updated_parsed, reverse=True)
    return combined_entries
rss_title = "### Recent Newsletter Issues by Jay Cuthrell on [fudge.org](https://fudge.org), [hot.fudge.org](https://hot.fudge.org), and [cuthrell.consulting](https://cuthrell.consulting)"
readme = Path('../_pages/newsletter.md').read_text()
# Fetch and combine feeds
feed1 = reverse_rss_feed("https://fudge.org/feed.xml")
feed2 = reverse_rss_feed("https://hot.fudge.org/rss")
feed3 = reverse_rss_feed("https://cuthrell.consulting/feed.xml")
combined_feed = combine_feeds(feed1, feed2, feed3)
posts = []
for item in combined_feed:
    title = item.title
    link = item.link
    published = (time.strftime('%Y %b %d', item.updated_parsed))
    posts.append(f" - [{title}]({link}) {published}")
posts_joined = '\n'.join(posts)
updated_readme = readme[:readme.find(rss_title)] + f"{rss_title}\n{posts_joined}"
with open('../_pages/newsletter.md', "w+") as f:
    f.write(updated_readme + update_footer())
