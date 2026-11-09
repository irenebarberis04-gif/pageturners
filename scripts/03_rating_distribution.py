# RQ2 - Rating Distributions
# How do readers' rating distributions differ across books?

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load the books dataset
books = pd.read_csv("data/raw (dati_grezzi)/books.csv")

# Define the columns containing the number of ratings for each star
rating_columns = [
    "ratings_1",
    "ratings_2",
    "ratings_3",
    "ratings_4",
    "ratings_5"
]

# Check missing values in the rating columns
print("\nMissing values in rating columns:")
print(books[rating_columns].isnull().sum())

# Calculate the total number of ratings for each book
books["total_ratings"] = books[rating_columns].sum(axis=1)

# Check whether any book has zero ratings
print("\nBooks with zero ratings:")
print((books["total_ratings"] == 0).sum())

# Check whether calculated totals match the original dataset
print("\nBooks with inconsistent rating totals:")
print(
    (books["total_ratings"] != books["work_ratings_count"]).sum()
)

# Keep books with valid rating totals
books = books[books["total_ratings"] > 0].copy()


# Calculate the percentage of ratings of each star rating for every book
for i in range(1, 6):
    books[f"pct_{i}_stars"] = (
        books[f"ratings_{i}"] / books["total_ratings"] * 100
    )


# Define the percentage columns
percentage_columns = [
    f"pct_{i}_stars" for i in range(1, 6)
]

# Display the first five books' rating percentages
print("\nRating percentages for the first 5 books:")
print(
    books[["title"] + percentage_columns]
    .head()
    .round(2)
    .to_string(index=False)
)


# Verify that the percentages sum to 100 for each book
books["total_percentage"] = books[percentage_columns].sum(axis=1)

print("\nSummary of total rating percentages:")
print(books["total_percentage"].describe().round(2))


# Overall rating distribution

# Count all ratings for each star across the dataset
overall_counts = books[rating_columns].sum()

# Calculate the total number of ratings across all books
overall_total = overall_counts.sum()

# Calculate the overall percentage for each star
overall_percentages = overall_counts / overall_total * 100

print("\nOverall rating distribution:")
for i in range(1, 6):
    print(
        f"{i} stars: {overall_percentages[f'ratings_{i}']:.2f}%"
    )

# Create a static bar chart of the overall distribution
stars = [1, 2, 3, 4, 5]

plt.figure(figsize=(9, 6))

plt.bar(
    stars,
    overall_percentages.values
)

plt.title("Overall Distribution of Star Ratings")
plt.xlabel("Star Rating")
plt.ylabel("Percentage of Ratings (%)")
plt.xticks(stars)
plt.ylim(0, 100)

plt.savefig(
    "figures/overall_rating_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# Rating distribution for an individual book

# Select a book by its position in the dataset
book = books.iloc[0]

# Extract its percentage of ratings for each star
percentages = [
    book[f"pct_{i}_stars"] for i in stars
]

print("\nSelected book:")
print(book["title"])
print("Author:", book["authors"])
print("Average rating:", book["average_rating"])

# Create an interactive Plotly bar chart
fig = px.bar(
    x=stars,
    y=percentages,
    title=f"Rating Distribution - {book['title']}",
    labels={
        "x": "Star Rating",
        "y": "Percentage of Ratings (%)"
    }
)

# Improve the chart layout
fig.update_layout(
    xaxis=dict(tickmode="array", tickvals=stars),
    yaxis=dict(range=[0, 100])
)

# Display the chart
fig.show()


# Export the data needed for the Streamlit application

app_columns = [
    "book_id",
    "title",
    "authors",
    "average_rating",
    "ratings_1",
    "ratings_2",
    "ratings_3",
    "ratings_4",
    "ratings_5"
]

books[app_columns].to_csv(
    "data/books_for_app.csv",
    index=False
)















