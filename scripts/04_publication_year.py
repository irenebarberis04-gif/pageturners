# RQ3 - Publication Year and Ratings

import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
books = pd.read_csv("data/raw (dati_grezzi)/books.csv")

# Remove books with missing publication years
books_with_year = books.dropna(
    subset=["original_publication_year"]
)

# Explore publication years
print("\nPublication year statistics:")
print(books_with_year["original_publication_year"].describe())

# Calculate the correlation between publication year and average rating

pearson_corr = books_with_year["original_publication_year"].corr(
    books_with_year["average_rating"]
)

spearman_corr = books_with_year["original_publication_year"].corr(
    books_with_year["average_rating"],
    method="spearman"
)

print("\nPearson correlation:", round(pearson_corr, 3))
print("Spearman correlation:", round(spearman_corr, 3))

# Visualize the relationship between publication year and average rating

plt.figure(figsize=(10, 6))

# Select books published from 1000 onwards
modern_books = books_with_year[
    books_with_year["original_publication_year"] >= 1000
]

# Create a scatter plot
plt.scatter(
    modern_books["original_publication_year"],
    modern_books["average_rating"],
    alpha=0.2,
    s=10,
)


plt.title("Publication year vs average rating")
plt.xlabel("Original publication year")
plt.ylabel("Average rating")

plt.savefig(
    "figures/publication_year_vs_rating.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# Select books published from 1800 onwards
books_1800 = books_with_year[
    books_with_year["original_publication_year"] >= 1800
].copy()

# Create a decade column
books_1800["decade"] = (
    books_1800["original_publication_year"] // 10 * 10
)

# Calculate the average rating for each decade
rating_by_decade = books_1800.groupby("decade")["average_rating"].mean()

print("\nAverage rating by decade:")
print(rating_by_decade.round(3))


# Count the number of books in each decade
books_per_decade = books_1800.groupby("decade").size()

print("\nNumber of books by decade:")
print(books_per_decade)

# Plot average rating by decade
plt.figure(figsize=(12, 6))

plt.scatter(
    rating_by_decade.index,
    rating_by_decade.values,
    s=books_per_decade.values / 5 + 15,
    alpha=0.6
)

plt.title("Average book rating by decade")
plt.xlabel("Publication decade")
plt.ylabel("Average rating")

plt.xticks(rating_by_decade.index, rotation=45)
plt.grid(alpha=0.3)

plt.figtext(
    0.5, -0.04,
    "Bubble size represents the number of books published in each decade",
    ha="center",
    fontsize=10
)

plt.savefig(
    "figures/average_rating_by_decade.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# Select books published between 1980 and 2016
recent_books = books_with_year[
    (books_with_year["original_publication_year"] >= 1980) &
    (books_with_year["original_publication_year"] <= 2016)
].copy()

# Calculate the average rating for each publication year
rating_by_year = recent_books.groupby(
    "original_publication_year"
)["average_rating"].mean()

print("\nAverage rating by year (1980-2016):")
print(rating_by_year.round(3))

# Count the number of books published each year
books_per_year = recent_books.groupby(
    "original_publication_year"
).size()

print("\nNumber of books by year (1980-2016):")
print(books_per_year)


# Plot average rating by publication year (1980-2016)

plt.figure(figsize=(12, 6))

plt.plot(
    rating_by_year.index,
    rating_by_year.values,
    marker="o",
    markersize=4
)

plt.title("Average book rating by publication year (1980-2016)")
plt.xlabel("Original publication year")
plt.ylabel("Average rating")

plt.grid(alpha=0.3)

plt.savefig(
    "figures/average_rating_by_year.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()







