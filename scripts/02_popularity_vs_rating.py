# RQ1 - Popularity vs Appreciation
# Analyze the relationship between the number of ratings
# a book receives and its average rating.

import pandas as pd
import matplotlib.pyplot as plt

# Load the books dataset
books = pd.read_csv("data/raw (dati_grezzi)/books.csv")

# 1. Descriptive statistics
popularity_data = books[["work_ratings_count", "average_rating"]]

print("Descriptive statistics for popularity and average rating:")
print(popularity_data.describe())

# 2. Pearson correlation
pearson_correlation = popularity_data[
    "work_ratings_count"
].corr(popularity_data["average_rating"])

print("\nPearson correlation:")
print(round(pearson_correlation, 3))

# 3. Scatter plot
plt.figure(figsize=(10, 6))

plt.scatter(
    popularity_data["work_ratings_count"],
    popularity_data["average_rating"],
    alpha=0.3
)

plt.xscale("log")
plt.title("Popularity vs Average Rating")
plt.xlabel("Number of Ratings (log scale)")
plt.ylabel("Average Rating")

plt.savefig(
    "figures/popularity_vs_rating.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# 4. Spearman correlation
spearman_correlation = popularity_data[
    "work_ratings_count"
].corr(
    popularity_data["average_rating"],
    method="spearman"
)

print("\nSpearman correlation:")
print(round(spearman_correlation, 3))