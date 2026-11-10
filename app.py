# Page Turners - Interactive Rating Distribution

import streamlit as st
import pandas as pd
import plotly.express as px

# Configure the Streamlit application
st.set_page_config(
    page_title="Page Turners",
    layout="wide"
)

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/books_for_app.csv")


books = load_data()

# Sidebar navigation
st.sidebar.title("Page Turners")

page = st.sidebar.radio(
    "Explore",
    [
        "Overview",
        "Popularity & Ratings",
        "Rating distributions",
        "Publication year"
    ]
)

# Page 1: Overview
if page == "Overview":

    st.title("Page Turners")
    st.subheader("What makes a book loved by readers?")

    st.write(
        "An exploratory data analysis of the Goodbooks-10k dataset, "
        "investigating how popularity, rating distributions, and "
        "publication year relate to readers' evaluations."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Books analyzed", f"{len(books):,}")

    with col2:
        st.metric("Research questions", "3")

    with col3:
        st.metric("Dataset", "Goodbooks-10k")

    st.subheader("Research questions")

    st.markdown(
        """
        **01 — Popularity & Ratings**

        Does a book's popularity relate to its average rating?

        **02 — Rating distributions**

        How do readers' rating distributions differ across books?

        **03 — Publication year**

        Does publication year influence average ratings?
        """
    )

# Page 2: Popularity & Ratings
elif page == "Popularity & Ratings":
    #page title and research question
    st.title("Popularity & Ratings")

    st.write(
        "Is a book's popularity associated with its average rating?"
    )

    st.divider()

    # Display correlation coefficients
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Pearson correlation", "0.045")

    with col2:
        st.metric("Spearman correlation", "0.065")

    st.divider()

    # Display the scatter plot
    st.subheader("Popularity vs average rating")

    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        st.image(
            "figures/popularity_vs_rating.png",
            use_container_width=True
        )

    # Display the main finding
    st.markdown(
        """
        **Conclusion**

        Popularity has a very weak association with average ratings.
        Books receiving more ratings do not necessarily receive higher scores.
        """
    )

    

# Page 3: Rating distributions
elif page == "Rating distributions":

    st.title("Rating distributions")

    st.write(
        "How do readers' rating distributions differ across books?"
    )

    st.divider()

    st.metric("4–5 Star Ratings", "73.31%")

    st.caption("Nearly three-quarters of all ratings are 4 or 5 stars.")

    st.divider()
    
    #interactive book selection
    st.subheader("Explore individual books")

    st.write("Select a book to explore its rating distribution.")

    books["book_label"] = books["title"] + " — " + books["authors"]

    books = books.sort_values("book_label")

    selected_id = st.selectbox(
        "Search by title or author:",
        options=books["book_id"].tolist(),
        format_func=lambda book_id: books.loc[
            books["book_id"] == book_id, "book_label"
        ].iloc[0]
    )

    selected_book = books[
        books["book_id"] == selected_id
    ].iloc[0]
    
    
    #selected book information
    st.subheader(selected_book["title"])

    st.caption(selected_book["authors"])

    st.metric(
        "Average rating",
        f"{selected_book['average_rating']:.2f} / 5"
    )
    
    
    #rating distribution calculation
    stars = [1, 2, 3, 4, 5]

    total_ratings = sum(
        selected_book[f"ratings_{i}"] for i in stars
    )

    percentages = [
        selected_book[f"ratings_{i}"] / total_ratings * 100
        for i in stars
    ]

    rating_distribution = pd.DataFrame({
        "Stars": stars,
        "Percentage": percentages
    })
    
    
    #Interactive rating distribution chart
    fig = px.bar(
        rating_distribution,
        x="Stars",
        y="Percentage",
        labels={
            "Stars": "Star rating",
            "Percentage": "Percentage of ratings (%)"
        },
        color_discrete_sequence=["#69B3E7"]
    )

    fig.update_layout(
        template="plotly_white",
        height=400,
        xaxis=dict(
            tickmode="array",
            tickvals=stars
        ),
        yaxis=dict(range=[0, 100]),
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        st.plotly_chart(fig, use_container_width=True)


    #conclusions
    st.markdown("""
    **Conclusions**

    Rating distributions vary considerably across books.
    Although high ratings dominate overall, individual books
    can show very different patterns of reader evaluations.
    """)

    
# Page 4: Publication Year
elif page == "Publication year":

    st.title("Publication year")

    st.write(
        "Does publication year influence average ratings?"
    )

    st.divider()

    # Display correlations calculated on the full dataset
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Pearson correlation", "0.016")

    with col2:
        st.metric("Spearman correlation", "-0.027")

    st.divider()

    st.subheader("Explore ratings over time")

    # Keep books with valid publication years from 1800 onwards
    year_data = books.dropna(
        subset=["original_publication_year"]
    ).copy()

    year_data = year_data[
        year_data["original_publication_year"] >= 1800
    ]

    # Allow users to select the publication period
    year_range = st.slider(
        "Publication period",
        min_value=1800,
        max_value=2017,
        value=(1980, 2016)
    )

    # Filter books according to the selected period
    filtered_books = year_data[
        year_data["original_publication_year"].between(
            year_range[0],
            year_range[1]
        )
    ].copy()

    # Allow users to choose how to group the data
    grouping = st.radio(
        "Group data by",
        ["Year", "Decade"],
        horizontal=True
    )

    if grouping == "Year":
        filtered_books["period"] = (
            filtered_books["original_publication_year"].astype(int)
        )

    else:
        filtered_books["period"] = (
            filtered_books["original_publication_year"] // 10 * 10
        ).astype(int)

    # Calculate average rating and number of books per period
    rating_over_time = filtered_books.groupby( 
        "period", as_index=False
    ).agg(
        average_rating=("average_rating", "mean"),
        book_count=("book_id", "count")
    )

    # Create the interactive chart
    fig = px.line(
        rating_over_time,
        x="period",
        y="average_rating",
        markers=True,
        hover_data={"book_count": True},
        labels={
            "period": "Publication year" if grouping == "Year" else "Publication decade",
            "average_rating": "Average rating",
            "book_count": "Number of books"
        }
    )

    fig.update_layout(
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Correlation coefficients refer to the full dataset. "
        "The chart updates according to the selected publication period."
    )

    st.markdown("""
    **Observations**

    Publication year has a very weak association with average ratings.
    Older and newer books do not show a clear overall difference
    in readers' evaluations.
    """)
