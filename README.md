# What makes a book loved by readers?

**Page Turners** is a Python data analysis project exploring Goodreads book ratings, popularity, and publication trends using the Goodbooks-10k dataset.

The project combines data exploration, statistical analysis, visualization, and an interactive Streamlit dashboard to investigate how readers evaluate books.

## Project overview
The aim of this project is to explore patterns in readers' ratings and understand how book popularity, rating distributions, and publication years relate to readers' evaluations.

The analysis uses Python libraries such as Pandas, NumPy, Matplotlib, and Plotly to process the data, calculate descriptive statistics, and create visualizations.
An interactive Streamlit application allows users to explore the results and compare individual books.

## Research questions
The project focuses on three main research questions:
1. **Popularity & ratings:** Is there a relationship between the number of ratings a book receives and its average rating?
2. **Rating distributions:** How are ratings distributed across the five rating levels, and how do these distributions differ between books?
3. **Publication year:** Is there a relationship between a book's publication year and its average rating?

## Dataset
The project uses the [Goodbooks-10k dataset](https://github.com/zygmuntz/goodbooks-10k), which contains metadata for approximately 10,000 books and nearly 6 million individual user ratings.
The dataset includes information about book titles, authors, publication years, average ratings, rating counts, and user-generated tags.
The analysis primarily uses `books.csv`, which contains book metadata and aggregated rating information.

## Analysis and key findings

### 1. Popularity & ratings
The relationship between the number of ratings and average book ratings is examined using descriptive statistics, Pearson correlation, and Spearman correlation.

The results show a negligible association between popularity and average rating:
- Pearson correlation: 0.045
- Spearman correlation: 0.065
This suggests that books receiving more ratings do not necessarily receive higher average ratings.

### 2. Rating distributions
The distribution of ratings from 1 to 5 stars is examined both across the dataset and for individual books.
Overall, higher ratings are more common, with approximately 73.31% of recorded ratings being either 4 or 5 stars.
The analysis also compares rating distributions across individual books through interactive visualizations.

### 3. Publication year
The relationship between publication year and average rating is investigated using correlation analysis and visualizations grouped by year and decade.

The overall correlations are close to zero:
- Pearson correlation: 0.016
- Spearman correlation: -0.027
These results indicate a negligible overall association between publication year and average rating, although some differences can be observed across individual years and decades.

For a more detailed explanation of the methodology and results, see [Analysis Documentation](analysis_datasets.md).

## Interactive streamlit application
An interactive dashboard was developed using Streamlit and Plotly to make the analysis accessible and easier to explore.

The application allows users to:
- Explore the relationship between book popularity and average ratings.
- Search for individual books by title or author and examine their rating distributions.
- Explore average ratings across publication years and decades.
- Select a publication-year interval and view dynamically calculated Pearson and Spearman correlations.

**Live application:** [Explore Page Turners](https://pageturners-apjsanp6cplbz5cwapjyd5.streamlit.app/)

## Technologies used
- Python
- Pandas and NumPy for data processing and analysis
- Matplotlib and Plotly for data visualization
- SciPy for statistical analysis
- Streamlit for the interactive application
- Git and GitHub for version control

## Installation and usage
Clone the repository:
```bash
git clone https://github.com/irenebarberis04-gif/pageturners.git
cd pageturners
```
### Dataset setup
Download the original CSV files from the [Goodbooks-10k repository](https://github.com/zygmuntz/goodbooks-10k) and place them in the following directory:
`data/raw (dati_grezzi)/`

The original datasets are excluded from version control due to their size.
The Streamlit application uses a separate, preprocessed dataset (`data/books_for_app.csv`)

Install the required Python libraries:
```bash
python -m pip install -r requirements.txt
```

Launch the interactive dashboard:
```bash
python -m streamlit run app.py
```

The application will open in a web browser.

## Documentation
Detailed information about data exploration, preparation, research methods, visualizations, and findings is available in [analysis_datasets.md](analysis_datasets.md).

