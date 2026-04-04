# Import libraries
import pandas as pd
import os
# File path to the collected JSON data (from task 1)
file_path = "data/trends_20260403.json"  
# Step 1: Load JSON file into DataFrame
df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")
# Step 2: Remove duplicates (based on post_id)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")
# Step 3: Remove missing values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Step 4: Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Step 5: Remove low quality (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Step 6: Remove extra whitespace in title
df["title"] = df["title"].str.strip()

# Step 7: Save as CSV

# Create folder if not exists
if not os.path.exists("data"):
    os.makedirs("data")

output_file = "data/trends_clean.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# Step 8: Summary - stories per category
print("\nStories per category:")
print(df["category"].value_counts())
