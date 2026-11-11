# Page Turners – Analysis Notes
## 1. Dataset exploration 
### 1.1 Books dataset (`books.csv`)

**Dataset dimensions**
- Rows: 10,000
- Columns: 23

**Relevant variables**
| Variable | Description |
|---|---|
| `book_id` | Dataset book identifier |
| `authors` | Book author(s) |
| `original_publication_year` | Original publication year |
| `title` | Book title |
| `average_rating` | Average book rating |
| `ratings_count` | Number of ratings |
| `work_ratings_count` | Number of ratings associated with the work |
| `ratings_1` – `ratings_5` | Number of ratings for each score |

**Missing values**
| Variable | Missing values |
|---|---:|
| `isbn` | 700 |
| `isbn13` | 585 |
| `original_title` | 585 |
| `original_publication_year` | 21 |
| `language_code` | 1,084 |
All other columns have no missing values.

### 1.2 Initial observations
- The dataset contains information about books, authors, publication years and reader ratings.
- `average_rating` can be used to investigate reader appreciation.
- `ratings_count` and `work_ratings_count` can help measure book popularity.
- Missing publication years will need to be considered before analyzing publication dates.


### 1.3 Ratings dataset (`ratings.csv`)

**Dataset dimensions**
- Rows: 5,976,479
- Columns: 3

**Variables**
| Variable | Description |
|---|---|
| `user_id` | Unique identifier of the user |
| `book_id` | Identifier of the rated book |
| `rating` | Rating assigned by the user (1–5) |

All three variables are stored as integers (`int64`).

**Descriptive statistics**
- Mean rating: 3.92
- Standard deviation: 0.99
- Minimum rating: 1
- Median rating: 4
- Maximum rating: 5

There are no missing values in this dataset.

**Initial observations**
- The dataset contains almost 6 million ratings.
- Ratings range from 1 to 5.
- The average rating is approximately 3.92, suggesting that ratings tend to be relatively positive.
- The dataset can be used to investigate user preferences and book popularity.


### 1.4 Book tags dataset (`book_tags.csv`)

**Dataset dimensions**
- Rows: 999,912
- Columns: 3

**Variables**
| Variable | Description |
|---|---|
| `goodreads_book_id` | Goodreads identifier of the book edition |
| `tag_id` | numerical identifier of the tag assigned to the book |
| `count` | Number of times users assigned the tag to the book |

All three variables are stored as integers (`int64`).

**Descriptive statistics**
- Mean count: 208.87
- Median count: 15
- Minimum count: -1
- Maximum count: 596,234

There are no missing values in this dataset.

**Initial observations**
- The dataset contains almost one million book-tag associations.
- `tag_id` contains numerical identifiers that need to be matched with `tags.csv` to identify the corresponding tag names.
- The mean count is considerably higher than the median, suggesting a highly uneven distribution.
- The minimum value of -1 will need further investigation during data cleaning.


### 1.5 Tags dataset (`tags.csv`)

**Dataset dimensions**
- Rows: 34,252
- Columns: 2

**Variables**
| Variable | Description |
|---|---|
| `tag_id` | Numerical identifier of the tag |
| `tag_name` | Textual name of the tag |

- `tag_id`: integer (`int64`)
- `tag_name`: string (`str`)

There are no missing values in this dataset.

**Initial observations**
- The dataset contains 34,252 different tag identifiers and their corresponding names.
- `tags.csv` can be used to translate the numerical `tag_id` values in `book_tags.csv` into readable labels.


### 1.6 To-read dataset (`to_read.csv`)

**Dataset dimensions**
- Rows: 912,705
- Columns: 2

**Variables**
| Variable | Description |
|---|---|
| `user_id` | Identifier of the user |
| `book_id` | Identifier of the work marked as "to read", corresponding to `work_id` in `books.csv` |

Both variables are stored as integers (`int64`).

There are no missing values in this dataset.

**Initial observations**
- The dataset contains 912,705 user-book associations.
- Each row represents a book marked as "to read" by a user.
- The dataset can be used to investigate users' reading interests and preferences.


## 2. Initial dataset relationships

### 2.1 Relationship between books and ratings

The relationship between `books.csv` and `ratings.csv` was checked using the `book_id` variable.

- Unique book IDs in `ratings.csv`: 10,000
- Unique book IDs in `books.csv`: 10,000
- All book IDs in `ratings.csv` are present in `books.csv`.

The check returned `True`, confirming that all rating records can be associated with a book in the books dataset using `book_id`.

This is a one-to-many relationship: each book can have multiple ratings from different users, while each rating record refers to one book.


### 2.2 Relationship between books and to_read

The relationship between `books.csv` and `to_read.csv` was checked using the `book_id` variable.

- Unique book IDs in `to_read.csv`: 9,986
- Unique book IDs in `books.csv`: 10,000
- All book IDs in `to_read.csv` are present in `books.csv`.

The check returned `True`, confirming that all to-read records can be associated with a book in the books dataset using `book_id`.

However, 14 books in `books.csv` do not appear in `to_read.csv`.


### 2.3 Relationship between books and book_tags

The relationship between `books.csv` and `book_tags.csv` was checked using the `goodreads_book_id` variable.

- Unique Goodreads book IDs in `book_tags.csv`: 10,000
- All Goodreads book IDs in `book_tags.csv` are present in `books.csv`.

The check returned `True`, confirming that all tag records can be associated with a book in the books dataset using `goodreads_book_id`.

This is a one-to-many relationship: each book can have multiple associated tags.


### 2.4 Relationship between book_tags and tags

The relationship between `book_tags.csv` and `tags.csv` was checked using the `tag_id` variable.

- Unique tag IDs in `book_tags.csv`: 34,252
- Unique tag IDs in `tags.csv`: 34,252
- All tag IDs in `book_tags.csv` are present in `tags.csv`.

The check returned `True`, confirming that all tag records can be associated with their corresponding tag names using `tag_id`.

This allows us to identify the tags assigned to each book and potentially use them to investigate differences in average ratings across genres.


## 3. Duplicate records analysis

### 3.1 Books
No fully duplicated rows or duplicated `book_id` values were found.
Each book has a unique identifier.

### 3.2 Ratings
No fully duplicated rows or duplicated combinations of `user_id` and `book_id` were found.
Each user-book combination appears at most once.

### 3.3 To-read
No fully duplicated rows or duplicated combinations of `user_id` and `book_id` were found.

### 3.4 Book tags
The initial analysis identified:
- 6 fully duplicated rows.
- 8 duplicated book-tag combinations.

The 6 fully duplicated rows were removed using `drop_duplicates()`.
The remaining 2 duplicated combinations have conflicting `count` values and were temporarily retained because the correct values could not be determined.
The cleaned dataset contains 999,906 rows.

### 3.5 Tags
No fully duplicated rows, duplicated `tag_id` values or duplicated `tag_name` values were found.
Each tag has a unique identifier and name.


## 4. Data Cleaning and Anomaly Checks

### 4.1 Missing Publication Years

- `books.csv` contains **21 missing values** in `original_publication_year`.
- A separate DataFrame, `books_with_year`, was created using `dropna(subset=["original_publication_year"])`.
- The resulting DataFrame contains **9,979 books**.
- The original `books` DataFrame was preserved for analyses not involving publication year.
- Missing ISBNs, original titles, and language codes were retained because they are not essential to the main research questions.

### 4.2 Publication Year Validation

- Publication years range from **-1750 to 2017**.
- **125 books** have publication years earlier than 1800.
- These records were retained because they largely correspond to historical and classical works.
- Publication years for ancient works may be approximate.

### 4.3 Rating and Popularity Validation

- `average_rating` ranges from **2.47 to 4.82**, with no values outside the valid 1–5 interval.
- `ratings_count` ranges from **2,716 to 4,780,653**, with no zero or negative values.
- No negative values were found in `ratings_1`, `ratings_2`, `ratings_3`, `ratings_4`, or `ratings_5`.
- No corrections were required for these variables.

### 4.4 Negative Tag Counts

- **6 records** in `book_tags` contained `count = -1`.
- The affected records belonged to **2 books**.
- The negative counts were associated with the tags `ebook`, `no-audio`, `kindle-library`, `challenge-2013`, `america-in-retreat`, and `default`.
- These records were removed because tag frequencies cannot be negative.
- After removing **6 exact duplicates** and **6 negative-count records**, `book_tags_clean` contains **999,900 rows**.
- Two book-tag pairs with conflicting positive counts were retained because the correct values could not be determined.

### 4.5 Rating Count Consistency

- The sum of `ratings_1` through `ratings_5` was calculated for each book and stored in `total_star_ratings`.
- This sum differed from `ratings_count` for **9,986 books**.
- However, it matched `work_ratings_count` for **all 10,000 books**.
- This confirms that the star-rating distributions correspond to **work-level ratings** rather than edition-level ratings.
- No corrections were required.

### 4.6 Final Cleaning Decisions

- Original datasets were preserved whenever possible.
- Missing publication years were excluded **only from year-based analyses**.
- Exact duplicates and invalid negative tag counts were removed.
- Valid historical publication years were retained.
- The cleaned `book_tags_clean` DataFrame contains **999,900 records**.
- `work_ratings_count` will be used as the **primary popularity measure** in the first research question.

**Conclusion:** The datasets have been checked for missing values, duplicates, invalid numerical values, and rating-count consistency. The data is now ready for exploratory and statistical analysis.


## RQ1 — Popularity vs. Appreciation

**Research question:** Is there a relationship between the number of ratings a book receives and its average rating?

**Variables:** `work_ratings_count` (popularity) and `average_rating` (appreciation).

**Methods:**
- Descriptive statistics using `describe()`.
- Pearson correlation to assess linear association.
- Scatter plot with a logarithmic x-axis to visualize the relationship.
- Spearman correlation to assess monotonic association.

**Results:**
- Pearson correlation: **0.045**.
- Spearman correlation: **0.065**.
- The scatter plot shows no clear increasing or decreasing trend.

**Conclusion:** Popularity and appreciation show very weak associations in this dataset. Books receiving more ratings do not necessarily achieve higher average ratings.

**Figure:**

![Popularity vs Average Rating](figures/popularity_vs_rating.png)


## RQ2 — Rating Distributions

**Research question:** How do readers' rating distributions differ across books?

### Data and Methods

The analysis focuses on five variables from `books.csv`:
- `ratings_1`
- `ratings_2`
- `ratings_3`
- `ratings_4`
- `ratings_5`

The total number of ratings was calculated by summing the five categories. The percentage of each rating category was obtained by dividing its count by the total number of ratings.

The analysis includes:
- Overall rating distribution from 1 to 5 stars.
- Percentage of positive ratings (4 and 5 stars).
- Comparison of rating distributions across individual books.

### Results

| Rating | Percentage |
|---|---:|
| 1 star | 2.25% |
| 2 stars | 5.21% |
| 3 stars | 19.23% |
| 4 stars | 33.45% |
| 5 stars | 39.86% |

Overall, **73.31% of ratings are 4 or 5 stars**, indicating that positive evaluations dominate the dataset.

However, rating distributions vary across individual books.

### Interactive Visualization

The Streamlit dashboard allows users to select a book by title or author and explore its rating distribution.

For each selected book, a Plotly bar chart displays the percentage of ratings from 1 to 5 stars. The book's average rating is also displayed.

This visualization helps identify differences between books that may not be immediately apparent from their average ratings alone.

### Conclusion

Positive ratings dominate the dataset, with **73.31% of evaluations receiving 4 or 5 stars**. However, rating distributions vary across books, showing that average ratings alone do not fully describe readers' evaluations.

---

## RQ3 — Publication Year vs Average Rating

**Research question:** Does a book's original publication year influence its average rating?

### Data Preparation
The analysis focuses on two variables from `books.csv`:
- `original_publication_year`: original publication year.
- `average_rating`: average Goodreads rating.

The original dataset contains **10,000 books**, of which **21 have missing publication years**.
After excluding these observations, **9,979 books** remained available for analysis.
All valid publication years were retained for the correlation analysis, while different time ranges were selected for visualization to improve readability.

### Statistical Analysis
Two correlation coefficients were calculated:
- **Pearson correlation: 0.016**
- **Spearman correlation: -0.027**
Both coefficients are close to zero, indicating a negligible overall linear or monotonic relationship between publication year and average rating.

### Visualizations

#### 1. Publication Year vs Average Rating
![Publication Year vs Average Rating](figures/publication_year_vs_rating.png)
A scatter plot was created to examine the relationship between publication year and average rating.
Only books published from the year 1000 onward were displayed to improve readability. No clear increasing or decreasing trend was observed.

#### 2. Average Rating by Decade
![Average Rating by Decade](figures/average_rating_by_decade.png)
Books published from 1800 onward were grouped by decade.
The chart displays the average rating for each decade, with bubble size representing the number of books.
Average ratings remain relatively stable, generally around 4 stars. Earlier decades contain fewer books, so their averages should be interpreted with caution.

#### 3. Average Rating by Publication Year (1980–2016)
![Average Rating by Publication Year](figures/average_rating_by_year.png)
A line chart displays annual average ratings between 1980 and 2016.
The year 2017 was excluded from this visualization because it contains only 11 books, although it remains included in the correlation analysis.
Some fluctuations are observed, but no consistent increasing or decreasing trend emerges.

### Animated Publication Year Chart
An interactive Plotly animation was created to show how average ratings evolve across publication years from 1980 to 2016.

**[Open the animated chart](figures/animated_publication_year.html)**

The animation includes a Play button that progressively displays the annual data.

This visualization was retained as part of the exploratory analysis but was not included in the Streamlit dashboard to keep the interface simple.


### Interactive Dashboard
An interactive Plotly line chart was implemented in Streamlit to explore the relationship between publication year and average rating.
Users can:
- Select a publication-year interval using a slider.
- Group the data by individual year or decade.
- Explore average ratings over time.
- View the number of books included in each period.
For each selected year or decade, the dashboard calculates the mean of the books' average ratings and the number of books.
The Pearson and Spearman correlations remain fixed because they refer to the full dataset with available publication years.

### Key Findings
- Publication year has a negligible overall correlation with average rating.
- Average ratings remain relatively stable across decades.
- Annual fluctuations exist, but no consistent temporal trend emerges.
- The number of books varies across publication periods, affecting the interpretation of group averages.

### Limitation
The Goodbooks-10k dataset is not representative of all published books.
Furthermore, the analysis uses book-level average ratings rather than individual reader ratings. Each book contributes equally to the yearly and decadal averages, regardless of how many ratings it received.

### Conclusion
There is no clear evidence of a strong overall relationship between a book's original publication year and its average Goodreads rating.
Older books are not systematically rated higher or lower than more recently published books in this dataset.












