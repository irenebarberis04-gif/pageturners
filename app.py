# Page Turners - Interactive Rating Distribution

import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration
st.set_page_config(
    page_title="Page Turners",
    layout="centered"
)

# Load the books dataset
books = pd.read_csv("data/books_for_app.csv")

# Display the app title
st.title("Page Turners")

# Display the research question
st.subheader("How Do Readers' Rating Distributions Differ Across Books?")

# Explain what the app does
st.write(
    "Select a book to explore the percentage of "
    "1-star to 5-star ratings it has received."
)

# Create a searchable list of books
books["book_label"] = (
    books["title"] + " — " + books["authors"]
)

# Sort books alphabetically
books = books.sort_values("book_label")

# Let the user select a book
selected_id = st.selectbox(
    "Search for a book by title or author:",
    options=books["book_id"].tolist(),
    format_func=lambda book_id: books.loc[
        books["book_id"] == book_id, "book_label"
    ].iloc[0]
)

# Get the selected book's information
selected_book = books[
    books["book_id"] == selected_id
].iloc[0]

# Display information about the selected book
st.subheader(selected_book["title"])

st.write("Author:", selected_book["authors"])

st.metric(
    "Average Rating",
    f"{selected_book['average_rating']:.2f} / 5"
)

# Define the possible star ratings
stars = [1, 2, 3, 4, 5]

# Calculate the total number of ratings for the selected book
total_ratings = sum(
    selected_book[f"ratings_{i}"] for i in stars
)

# Calculate the percentage of each star rating
percentages = [
    selected_book[f"ratings_{i}"] / total_ratings * 100
    for i in stars
]

# Create a DataFrame for the chart
rating_distribution = pd.DataFrame({
    "Stars": stars,
    "Percentage": percentages
})

# Create the interactive bar chart
fig = px.bar(
    rating_distribution,
    x="Stars",
    y="Percentage",
    title="Rating Distribution",
    labels={
        "Stars": "Star Rating",
        "Percentage": "Percentage of Ratings (%)"
    },
    color_discrete_sequence=["#69B3E7"]
)

# Improve the chart appearance
fig.update_layout(
    template="plotly_white",
    xaxis=dict(tickmode="array", tickvals=stars),
    yaxis=dict(range=[0, 100])
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
