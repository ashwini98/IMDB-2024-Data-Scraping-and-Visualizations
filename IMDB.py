import streamlit as st
import pandas as pd
import mysql.connector
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load data from CSV
combinedf = pd.read_csv(r'D:\AP\combined_data.csv')

# SQL connection
mydb = mysql.connector.connect(
    host="localhost",      # Update with your MySQL host
    user="root",           # Update with your MySQL username
    password="",           # Update with your MySQL password
    port=3306,             # Update if necessary
    autocommit=True        # Automatically commit the changes
)
mycursor = mydb.cursor(buffered=True)

# Create Database and Table if not exists
mycursor.execute("CREATE DATABASE IF NOT EXISTS IMDB20")
mycursor.execute("USE IMDB20")

# Create a table to store movie data 
mycursor.execute(""" 
    CREATE TABLE IF NOT EXISTS movies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        movie_name VARCHAR(255),
        rating DECIMAL(3, 1),
        votes INT,
        duration INT,
        genre VARCHAR(255)
    )
""")

# Insert data into the database only once, if necessary to avoid data loading multiple times into the database while running the app or script

def insert_data():
    for index, row in combinedf.iterrows():
        mycursor.execute("""
            INSERT INTO movies (`movie_name`, `rating`, `votes`, `duration`, `genre`)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE movie_name=VALUES(movie_name)  -- Prevent inserting duplicates
        """, (row['Movie Name'], row['Rating'], row['Votes'], row['Duration'], row['Genre']))
    mydb.commit()
    st.write("Data has been successfully inserted into the database!")

# Querying the database:
# Sidebar radio button to toggle between Movie Data, Filtered Data, and Visualization Data
selected_view = st.sidebar.radio("Choose:", ["Movie Data 2024", "Movie Filter 1","Movie Filter 2", "Data Visualization"])

if selected_view == "Movie Data 2024":
    
    # Insert data button to trigger insert once
    if st.button("Insert Data into DB"):
        insert_data()
    # Display data from the database
    st.title('IMDb Movies 2024')
    st.write(combinedf)
    

elif selected_view == "Movie Filter 1":
    
    # Basic Filter with Genre, Rating, Votes, Duration
    st.title("Filter Movies")
    # Filter by Genre using multiselect
    genre_options = combinedf['Genre'].unique().tolist()
    genre_filter = st.multiselect("Filter by Genre", genre_options, default=["Action"])
    
    # Duration filter options
    duration_options = ['< 2 hrs', '2-3 hrs', '> 3 hrs']
    selected_duration = st.multiselect("Select Duration", duration_options, default=['> 3 hrs'])
    
    # Rating filter slider
    rating_options = st.slider("Minimum IMDb Rating", 0.0, 10.0, 5.0, 0.1)  # Min, Max, Default, Step
    
    # Votes filter
    votes_options = st.number_input("Minimum Votes", min_value=0, value=50000)
    # SQL query construction based on filters
    filter_query = """
        SELECT id, movie_name, duration, rating, votes, genre
        FROM movies
        WHERE 1=1
    """
    
    # Genre filter
    if genre_filter:
        genre_list = ', '.join([f"'{genre}'" for genre in genre_filter])
        filter_query += f" AND genre IN ({genre_list})"
    
    # Duration filter
    if '< 2 hrs' in selected_duration:
        filter_query += " AND duration < 120"
    if '2-3 hrs' in selected_duration:
        filter_query += " AND duration BETWEEN 120 AND 180"
    if '> 3 hrs' in selected_duration:
        filter_query += " AND duration > 180"
    
    # Rating filter
    filter_query += f" AND rating >= {rating_options}"
    
    # Votes filter
    filter_query += f" AND votes >= {votes_options}"
    
    # Print the SQL query for debugging purposes
    st.write(f"SQL Query: {filter_query}")

    # Execute the query and fetch results
    try:
        mycursor.execute(filter_query)
        filtered_data = mycursor.fetchall()
        # Convert the results into a DataFrame
        columns = ['ID', 'Movie Name', 'Duration', 'Rating', 'Votes', 'Genre']
        filtered_df = pd.DataFrame(filtered_data, columns=columns)
        # Display the filtered data as a table
        if len(filtered_df) > 0:
            st.dataframe(filtered_df)
        else:
            st.write("No movies found based on your filters.")
    except Exception as e:
        st.write(f"Error occurred: {str(e)}")

elif selected_view == "Movie Filter 2":
    st.title("Advanced Movie Filters Search")
    select_view = st.radio("Filter By:", ["Genre", "Duration","Rating", "Votes"])
    
    if select_view == "Genre":
        # Filter by Genre
        st.subheader("Genre Filter")
        genre_options = combinedf['Genre'].unique().tolist()
        genre_filter = st.multiselect("Filter by Genre", genre_options, default=["Action", "Adventure"])
        
        # Genre Filter Query and Display
        genre_filter_query = """
            SELECT id, movie_name, duration, rating, votes, genre 
            FROM movies
            WHERE genre IN ({})
        """.format(', '.join([f"'{genre}'" for genre in genre_filter]))
        
        try:
            mycursor.execute(genre_filter_query)
            genre_filtered_data = mycursor.fetchall()
            genre_filtered_df = pd.DataFrame(genre_filtered_data, columns=['ID', 'Movie Name', 'Duration', 'Rating', 'Votes', 'Genre'])
            if len(genre_filtered_df) > 0:
                st.write(f"Movies filtered by Genre: {', '.join(genre_filter)}")
                st.dataframe(genre_filtered_df)
            else:
                st.write("No movies found based on genre filter.")
        except Exception as e:
            st.write(f"Error occurred in genre filter: {str(e)}")
    
    elif select_view == "Votes":
        # Filter by Votes
        st.subheader("Votes Filter")
        votes_filter = st.number_input("Minimum Votes", min_value=0, value=50000)
        
        # Votes Filter Query and Display
        votes_filter_query = """
            SELECT id, movie_name, duration, rating, votes, genre
            FROM movies
            WHERE votes >= {}
        """.format(votes_filter)
        
        try:
            mycursor.execute(votes_filter_query)
            votes_filtered_data = mycursor.fetchall()
            votes_filtered_df = pd.DataFrame(votes_filtered_data, columns=['ID', 'Movie Name', 'Duration', 'Rating', 'Votes', 'Genre'])
            if len(votes_filtered_df) > 0:
                st.write(f"Movies filtered by Votes ≥ {votes_filter}")
                st.dataframe(votes_filtered_df)
            else:
                st.write("No movies found based on votes filter.")
        except Exception as e:
            st.write(f"Error occurred in votes filter: {str(e)}")
    
    elif select_view == "Duration":
        # Filter by Duration
        st.subheader("Duration Filter")
        duration_options = ['< 2 hrs', '2-3 hrs', '> 3 hrs']
        selected_duration = st.multiselect("Select Duration", duration_options, default=['2-3 hrs'])
        
        # Duration Filter Query and Display
        duration_filter_query = """
            SELECT id, movie_name, duration, rating, votes, genre
            FROM movies
            WHERE 1=1
        """
        
        # Adding the selected duration filter
        if '< 2 hrs' in selected_duration:
            duration_filter_query += " AND duration < 120"
        if '2-3 hrs' in selected_duration:
            duration_filter_query += " AND duration BETWEEN 120 AND 180"
        if '> 3 hrs' in selected_duration:
            duration_filter_query += " AND duration > 180"
        
        try:
            mycursor.execute(duration_filter_query)
            duration_filtered_data = mycursor.fetchall()
            duration_filtered_df = pd.DataFrame(duration_filtered_data, columns=['ID', 'Movie Name', 'Duration', 'Rating', 'Votes', 'Genre'])
            if len(duration_filtered_df) > 0:
                st.write(f"Movies filtered by Duration: {', '.join(selected_duration)}")
                st.dataframe(duration_filtered_df)
            else:
                st.write("No movies found based on duration filter.")
        except Exception as e:
            st.write(f"Error occurred in duration filter: {str(e)}")
    
    elif select_view == "Rating":
        # Filter by Rating
        st.subheader("Rating Filter")
        rating_filter = st.slider("Minimum IMDb Rating", 0.0, 10.0, 0.0, 0.1)
        
        # Rating Filter Query and Display
        rating_filter_query = """
            SELECT id, movie_name, duration, rating, votes, genre
            FROM movies
            WHERE rating >= {}
        """.format(rating_filter)
        
        try:
            mycursor.execute(rating_filter_query)
            rating_filtered_data = mycursor.fetchall()
            rating_filtered_df = pd.DataFrame(rating_filtered_data, columns=['ID', 'Movie Name', 'Duration', 'Rating', 'Votes', 'Genre'])
            if len(rating_filtered_df) > 0:
                st.write(f"Movies filtered by Rating ≥ {rating_filter}")
                st.dataframe(rating_filtered_df)
            else:
                st.write("No movies found based on rating filter.")
        except Exception as e:
            st.write(f"Error occurred in rating filter: {str(e)}")

elif selected_view == "Data Visualization":  
    # Data Visualization
    # Top 10 Movies by Rating and Voting Counts:
    st.title("Top 10 Movies by Ratings and Votes")
    top_movies = combinedf.sort_values(by=['Votes', 'Rating'], ascending=False).head(10)
    st.write(top_movies)
    
    # Genre Distribution:     
    st.title("Genre Distribution")
    genre_counts = combinedf['Genre'].value_counts()   
    plt.figure(figsize=(10, 6))
    genre_counts.plot(kind='bar', color='skyblue')  
    plt.title('Movie Count per Genre', fontsize=16)
    plt.xlabel('Genre', fontsize=14)
    plt.ylabel('Number of Movies', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.tight_layout()
    st.pyplot(plt)

    # Average Duration by Genre:
    avg_duration_by_genre = combinedf.groupby('Genre')['Duration'].mean().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    avg_duration_by_genre.plot(kind='bar', color='lightgreen')  
    plt.title('Average Movie Duration per Genre', fontsize=16)
    plt.xlabel('Average Duration (Minutes)', fontsize=14)
    plt.ylabel('Genre', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.tight_layout()
    st.pyplot(plt)

    # Rating Distribution: Histogram/Boxplot
    # Histogram
    plt.figure(figsize=(10, 6))
    combinedf['Rating'].plot(kind='hist', bins=20, color='lightgreen', edgecolor='black') 
    plt.title('Distribution of Movie Ratings', fontsize=16)
    plt.xlabel('Rating', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.tight_layout()
    st.pyplot(plt)
    
    # Boxplot
    plt.figure(figsize=(10, 6))
    combinedf['Rating'].plot(kind='box', vert=False, color='skyblue') 
    plt.title('Boxplot of Movie Ratings', fontsize=16)
    plt.xlabel('Rating', fontsize=14)
    plt.tight_layout()
    st.pyplot(plt)

    # Most Popular Genres by Voting:
    total_votes_by_genre = combinedf.groupby('Genre')['Votes'].sum().reset_index()
    fig = px.pie(total_votes_by_genre, 
                 names='Genre', 
                 values='Votes', 
                 title='Most Popular Genres by Total Voting Counts',
                 color='Genre', 
                 color_discrete_sequence=px.colors.qualitative.Pastel)  
    st.plotly_chart(fig)

    # Duration Extremes:
    shortest_movie = combinedf.loc[combinedf['Duration'].idxmin()]
    longest_movie = combinedf.loc[combinedf['Duration'].idxmax()]   
    st.title("Shortest and Longest Movies")
    st.subheader("Shortest Movie")
    st.write(shortest_movie[['Movie Name', 'Duration', 'Genre', 'Rating', 'Votes']])
    st.subheader("Longest Movie")
    st.write(longest_movie[['Movie Name', 'Duration', 'Genre', 'Rating', 'Votes']])

    # Ratings by Genre: Heatmap of Average Ratings
    avg_ratings_by_genre = combinedf.groupby('Genre')['Rating'].mean().sort_values(ascending=False)
    rating_matrix = avg_ratings_by_genre.to_frame().T  
    plt.figure(figsize=(10, 6))
    sns.heatmap(rating_matrix, annot=True, cmap='Blues', cbar=True, linewidths=0.5)
    plt.title('Average Ratings by Genre')
    plt.tight_layout()
    st.pyplot(plt)

    # Correlation Analysis: Scatter Plot Between Ratings and Voting Counts
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Votes', y='Rating', data=combinedf, color='purple')
    plt.title('Correlation between Ratings and Voting Counts')
    plt.xlabel('Voting Counts')
    plt.ylabel('Rating')
    plt.tight_layout()
    st.pyplot(plt)

# Close the cursor and connection 
mycursor.close()
mydb.close()
