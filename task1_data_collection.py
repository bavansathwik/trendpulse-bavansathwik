# Import required libraries
import requests
import time
import json
import os
from datetime import datetime

# Base URLs for HackerNews API
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Headers (as given in question)
headers = {"User-Agent": "TrendPulse/1.0"}

# Categories and keywords
categories = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category based on title
def assign_category(title):
    title_lower = title.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return "others"


# Step 1: Fetch top story IDs
try:
    response = requests.get(TOP_STORIES_URL, headers=headers)
    story_ids = response.json()[:500]  # first 500
except Exception as e:
    print("Error fetching top stories:", e)
    story_ids = []

# Store collected data
all_stories = []

# Track count per category (max 25 each)
category_count = {cat: 0 for cat in categories}

# Step 2: Fetch each story
for story_id in story_ids:
    try:
        res = requests.get(ITEM_URL.format(story_id), headers=headers)
        story = res.json()

        # Skip if no title
        if not story or "title" not in story:
            continue

        title = story.get("title", "")
        category = assign_category(title)

        # Skip if category limit reached
        if category in category_count and category_count[category] >= 25:
            continue

        # Extract required fields
        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "unknown"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        all_stories.append(story_data)

        # Increase category count
        if category in category_count:
            category_count[category] += 1

        # Stop if all categories filled
        if all(count >= 25 for count in category_count.values()):
            break

    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        continue

# Step 3: Save to JSON file

# Create data folder if not exists
if not os.path.exists("data"):
    os.makedirs("data")

# File name with date
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

# Save file
with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_stories, f, indent=4)

# Final output
print(f"Collected {len(all_stories)} stories. Saved to {filename}")