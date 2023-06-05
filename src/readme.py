from pathlib import Path
import datetime
import time
import feedparser
import pytz

def update_footer():
    timestamp = datetime.datetime.now(pytz.timezone("America/New_York")).strftime("%c")
    footer = Path('../FOOTER.md').read_text()
    return footer.format(timestamp=timestamp)

def update_readme_buttondown_posts(buttondown_feed, readme_base, join_on):
    d = feedparser.parse(buttondown_feed)
    posts = []
    for item in d.entries:
            published = (time.strftime(' %Y %b %d',item.published_parsed))
            posts.append(f" - [{item['title']}]({item['link']}) {published}")
    posts_joined = '\n'.join(posts)
    return readme_base[:readme_base.find(rss_title)] + f"{join_on}\n{posts_joined}"

rss_title = "### Recent Newsletter Issues by Jay Cuthrell on [fudge.org](https://fudge.org)" # Anchor for where to append posts
readme = Path('../_pages/newsletter.md').read_text()
updated_readme = update_readme_buttondown_posts("https://fudge.org/rss.xml", readme, rss_title)
with open('../README.md', "w+") as f:
    f.write(updated_readme + update_footer())
