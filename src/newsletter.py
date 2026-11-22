from pathlib import Path
import datetime
import time
import feedparser
import pytz

# ==============================================================================
# Configuration & Adjustable Parameters
# ==============================================================================

# File paths resolved relative to this script's location in /src
SRC_DIR = Path(__file__).parent
PROJECT_ROOT = SRC_DIR.parent
NEWSLETTER_PATH = PROJECT_ROOT / "_pages" / "newsletter.md"
FOOTER_PATH = PROJECT_ROOT / "FOOTER.md"

# Timezone used for the footer build timestamp
TIMEZONE = "America/New_York"

# Stable anchor prefix used to locate where the dynamic list begins in newsletter.md.
# Using a short, stable prefix prevents .find() from returning -1 if links change.
SECTION_ANCHOR = "### Recent Newsletter Issues"

# Full Markdown heading written immediately above the generated post list
RSS_HEADING = (
    "### Recent Newsletter Issues by Jay Cuthrell on "
    "[fudge.org](https://fudge.org), "
    "[hot.fudge.org](https://hot.fudge.org), and "
    "[cuthrell.consulting](https://cuthrell.consulting)"
)

# List of (feed_url, feed_type) tuples to fetch and merge
FEED_SOURCES = [
    ("https://fudge.org/feed.xml", "blog"),
    # duplicative ("https://www.youtube.com/feeds/videos.xml?channel_id=UC0gbzQXghnt-4cgci-VpodQ", "podcast"),
    ("https://cuthrell.consulting/feed.xml", "blog"),
]

# Maps each feed_type to its display emoji
EMOJI_MAP = {
    "blog": "📝",
    "podcast": "🎙️",
}

# Optional: Set to an integer (e.g., 50) to limit total posts, or None for all posts
MAX_POSTS = None


# ==============================================================================
# Helper Functions
# ==============================================================================

def update_footer() -> str:
    """Reads FOOTER.md and injects the current timestamp in Eastern Time."""
    timestamp = datetime.datetime.now(pytz.timezone(TIMEZONE)).strftime("%c")
    footer_template = FOOTER_PATH.read_text(encoding="utf-8")
    return footer_template.format(timestamp=timestamp)


def get_entry_timestamp(entry) -> time.struct_time | None:
    """Safely extracts a parsed date tuple from an RSS/Atom entry."""
    return entry.get("updated_parsed") or entry.get("published_parsed")


def fetch_rss_entries(rss_feed_url: str) -> list:
    """Fetches and parses a single RSS/Atom feed with diagnostic logging."""
    parsed_feed = feedparser.parse(rss_feed_url)

    status = getattr(parsed_feed, "status", "unknown")
    if parsed_feed.bozo:
        print(f"Warning: Feed parser flagged an issue for {rss_feed_url} (HTTP {status}): {parsed_feed.bozo_exception}")

    entries = parsed_feed.entries or []
    print(f"Fetched {len(entries)} entries from {rss_feed_url} (HTTP {status})")
    return entries


def combine_feeds(feed_sources: list[tuple[str, str]]) -> list:
    """Fetches, deduplicates, and sorts entries from all configured feeds (newest first)."""
    combined_entries = []
    seen_links = set()

    for feed_url, feed_type in feed_sources:
        for entry in fetch_rss_entries(feed_url):
            link = entry.get("link", "").strip()
            parsed_date = get_entry_timestamp(entry)

            # Skip entries missing a URL or valid publication date
            if not link or parsed_date is None:
                continue

            # Avoid duplicate items if multiple feeds syndicate the same post
            if link in seen_links:
                continue

            seen_links.add(link)
            entry["feed_type"] = feed_type
            entry["normalized_date"] = parsed_date
            combined_entries.append(entry)

    combined_entries.sort(key=lambda item: item["normalized_date"], reverse=True)

    if MAX_POSTS is not None:
        return combined_entries[:MAX_POSTS]
    return combined_entries


def format_post_line(item) -> str:
    """Formats a single feed entry into a safe Markdown bullet item."""
    raw_title = item.get("title", "Untitled").strip()
    # Escape square brackets so titles do not break Markdown [title](url) syntax
    safe_title = raw_title.replace("[", "\\[").replace("]", "\\]")
    link = item.get("link", "").strip()
    published = time.strftime("%Y %b %d", item["normalized_date"])
    emoji = EMOJI_MAP.get(item.get("feed_type", ""), "")

    return f" - {emoji} [{safe_title}]({link}) {published}"


def build_newsletter_markdown(existing_content: str, posts: list[str]) -> str:
    """Replaces everything from SECTION_ANCHOR onward with the fresh post list and footer."""
    anchor_index = existing_content.find(SECTION_ANCHOR)

    # Fail loudly instead of slicing at -1 if the anchor heading is missing
    if anchor_index == -1:
        raise ValueError(
            f"Could not find anchor '{SECTION_ANCHOR}' in {NEWSLETTER_PATH}. "
            "Verify that _pages/newsletter.md contains this heading before running."
        )

    if not posts:
        raise ValueError("Zero valid entries were fetched across all feeds; aborting write to keep existing page intact.")

    static_header = existing_content[:anchor_index]
    posts_joined = "\n".join(posts)

    # Wrap generated entries in {% raw %} so Jekyll's Liquid engine ignores {{ or {% in titles
    dynamic_section = (
        f"{RSS_HEADING}\n\n"
        "{% raw %}\n"
        f"{posts_joined}\n"
        "{% endraw %}\n\n"
    )

    return static_header + dynamic_section + update_footer()


# ==============================================================================
# Main Execution
# ==============================================================================

if __name__ == "__main__":
    newsletter_content = NEWSLETTER_PATH.read_text(encoding="utf-8")
    combined_feed = combine_feeds(FEED_SOURCES)
    formatted_posts = [format_post_line(item) for item in combined_feed]

    updated_newsletter = build_newsletter_markdown(newsletter_content, formatted_posts)
    NEWSLETTER_PATH.write_text(updated_newsletter, encoding="utf-8")
    print(f"Successfully updated {NEWSLETTER_PATH} with {len(formatted_posts)} entries.")