# IMDB 2024 Data Scraping and Visualizations

## Overview
This project focuses on scraping, cleaning, filtering, and visualizing IMDB data to extract meaningful insights about movies, ratings, genres, and other related attributes. The goal is to explore trends, patterns, and correlations within the data to better understand the dynamics of the movie industry.

## Objectives
- Scrape IMDB data using **Selenium**.
- Perform data cleaning and preprocessing to handle missing or inconsistent data.
- Analyze movie ratings, genres, and release years to identify trends.
- Build interactive filter applications using **Streamlit**.
- Use **SQL** queries to filter and analyze data.
- Visualize data using graphs and charts for better interpretation.

## Tools and Technologies
- **Selenium**: For web scraping IMDB data.
- **Python**: Core programming language for data processing.
- **Pandas**: For data manipulation and cleaning.
- **Streamlit**: To build interactive filter applications.
- **SQL**: For storing, querying, and filtering data.
- **Matplotlib / Seaborn/Plotly**: For data visualization and charting.
- **Jupyter Notebook / VS Code**: For data analysis and exploration.

## Dataset
The dataset used in this project is sourced from IMDB and contains information about movies, including:
- **Title**
- **Genre**
- **IMDB Rating**
- **Number of Votes**
- **Duration**
- 

## Features
- **Data Scraping**: Extract movie data from IMDB using Selenium.
- **Data Cleaning**: Handle missing values, duplicates, and inconsistent data.
- **Data Filtering**: Build interactive filters for exploring the dataset and use SQL queries for advanced filtering.
- **Visualization**: Generate insightful visualizations to highlight key findings.
- **Insights**: Provide actionable insights for stakeholders in the movie industry.

## Deliverables
- Cleaned and preprocessed dataset.
- Interactive filter applications built with Streamlit.
- SQL queries for filtering and analyzing data.
- Visualizations showcasing trends and patterns.
- A comprehensive report summarizing findings and insights.

## How to Run
1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/imdb-2024-data-scraping.git
    cd imdb-2024-data-scraping
    ```
2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Run the Selenium script** to scrape IMDB data:
    ```bash
    python scrape_imdb_data.py
    ```
4. **Open the Jupyter Notebook** or **VS Code**:
    - Open `data_analysis.ipynb` or use VS Code to analyze the scraped data, clean it, and perform various analyses.
    - Run the steps in the notebook to clean, filter, and explore the dataset.
5. **Use SQL queries**:
    - Use SQL queries to filter and analyze the data further.
    - The dataset is stored in a local database for querying.
6. **Launch the Streamlit application**:
    ```bash
    streamlit run app.py
    ```
    - This will open the interactive dashboard where you can filter and visualize the dataset.

## Future Scope
- Extend the analysis to include **TV shows** and **web series**.
- Incorporate additional datasets (e.g., box office earnings, production budgets) for a more comprehensive study.
- Develop a **web application** to showcase the analysis interactively.

## Acknowledgements
- Special thanks to **IMDB** for providing a rich dataset for this project.
- Inspiration and resources from various Python libraries like Pandas, Matplotlib, Seaborn, and Streamlit.


