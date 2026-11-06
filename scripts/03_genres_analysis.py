# RQ2 - Genres, Popularity and Ratings
# Analyze which literary genres receive the highest average ratings
# and which genres are the most popular among readers.

import pandas as pd

# Load the datasets
books = pd.read_csv("data/raw (dati_grezzi)/books.csv")
book_tags = pd.read_csv("data/raw (dati_grezzi)/book_tags.csv")
tags = pd.read_csv("data/raw (dati_grezzi)/tags.csv")

# Clean book tags
book_tags_clean = book_tags.drop_duplicates()
book_tags_clean = book_tags_clean[
    book_tags_clean["count"] >= 0
].copy()

# Check dataset dimensions
print("Books:", books.shape)
print("Book tags:", book_tags_clean.shape)
print("Tags:", tags.shape)


# Identify the most frequently used tags
tag_frequency = (
    book_tags_clean
    .groupby("tag_id")["count"]
    .sum()
    .reset_index()
)

# Add tag names
tag_frequency = tag_frequency.merge(
    tags,
    on="tag_id",
    how="left"
)

# Select the 20 most frequently used tags
top_tags = tag_frequency.sort_values(
    "count", ascending=False
).head(20)

print("\nTop 20 most frequently used tags:")
print(top_tags[["tag_name", "count"]].to_string(index=False))






