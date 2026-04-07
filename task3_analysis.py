# Import libraries
import pandas as pd
import numpy as np

# 1. LOAD AND EXPLORE DATA

# Load CSV file from Task 2
df = pd.read_csv("data/trends_clean.csv")

# Print shape (rows, columns)
print(f"Loaded data: {df.shape}\n")

# Print first 5 rows
print("First 5 rows:")
print(df.head(), "\n")

# Calculate averages using pandas
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"Average score : {int(avg_score):,}")
print(f"Average comments: {int(avg_comments):,}\n")

# 2. BASIC ANALYSIS WITH NUMPY

# Convert to NumPy arrays
scores = df["score"].to_numpy()

# Calculate statistics
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

max_score = np.max(scores)
min_score = np.min(scores)

print("--- NumPy Stats ---")
print(f"Mean score   : {int(mean_score):,}")
print(f"Median score : {int(median_score):,}")
print(f"Std deviation: {int(std_score):,}")
print(f"Max score    : {int(max_score):,}")
print(f"Min score    : {int(min_score):,}\n")


# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"Most stories in: {top_category} ({top_count} stories)\n")


# Story with most comments
max_comments_row = df.loc[df["num_comments"].idxmax()]

print(f'Most commented story: "{max_comments_row["title"]}" '
      f'- {max_comments_row["num_comments"]:,} comments\n')


# 3. ADD NEW COLUMNS

# Engagement = comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if score > average score
df["is_popular"] = df["score"] > avg_score

# 4. SAVE RESULT

# Save updated CSV
df.to_csv("data/trends_analysed.csv", index=False)

print("Saved to data/trends_analysed.csv")