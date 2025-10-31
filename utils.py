import pandas as pd
import matplotlib.pyplot as plt


def change_release_date_format(movies_df):
    movies_df['release_date'] = pd.to_datetime(
        movies_df['release_date'])


def load_movies_data(filename="tmdb_movies.csv"):
    """
    Load movies data from a CSV file into a pandas DataFrame.

    Args:
        filename (str): The name of the CSV file to load.

    Returns:
        pd.DataFrame: A DataFrame containing the movies data, or None if an error occurred.
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        movies_df = pd.read_csv(filename)
        change_release_date_format(movies_df)
        return movies_df
    except FileNotFoundError as e:
        raise FileNotFoundError from e  # Ponownie zgłoś wyjątek
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError from e  # Ponownie zgłoś wyjątek
    except Exception as e:
        return None


def load_genres_data(filename="tmdb_genres.csv"):
    """
    Load genres data from a CSV file into a pandas DataFrame.

    Args:
        filename (str): The name of the CSV file to load.

    Returns:
        pd.DataFrame: A DataFrame containing the genres data, or None if an error occurred.
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    try:
        genres_df = pd.read_csv(filename)
        return genres_df
    except FileNotFoundError as e:
        raise FileNotFoundError from e  # Ponownie zgłoś wyjątek
    except pd.errors.EmptyDataError as e:
        raise pd.errors.EmptyDataError from e  # Ponownie zgłoś wyjątek
    except Exception as e:
        return None


def get_top_rated_movies(movies_df, top_n=10):
    """
    Get the top N rated movies based on vote average and vote count.

    Args:
    movies_df (pd.DataFrame): A DataFrame containing the movies data.
    top_n (int): The number of top rated movies to return.

    Returns:
    pd.DataFrame: A DataFrame containing the top N rated movies.
    """
    if movies_df is None or movies_df.empty:
        return pd.DataFrame()  # Zwróć pusty DataFrame, jeśli wejściowy jest pusty

    Q3 = movies_df['vote_count'].quantile(0.75)

    popular_movies = movies_df[movies_df['vote_count'] > Q3]
    top_n_movies = popular_movies.sort_values(
        by='vote_average', ascending=False).head(top_n)

    if popular_movies.empty:
        return pd.DataFrame()
    return top_n_movies.reset_index(drop=True)


def get_movies_year_range(movies_df, start_year, end_year):
    """
    Get movies released within a specified year range.

    Args:
    movies_df (pd.DataFrame): A DataFrame containing the movies data.
    start_year (int): The start year of the range.
    end_year (int): The end year of the range.

    Returns:
    pd.DataFrame: A DataFrame containing movies released within the specified year range.
    """
    if movies_df is None:
        print("Movies DataFrame is None.")
        return None

    mask = (movies_df['release_date'].dt.year >= start_year) & (
        movies_df['release_date'].dt.year <= end_year)
    movies_in_range = movies_df.loc[mask]
    return movies_in_range.reset_index()


def million(x, pos):
    return '{:2.1f}M'.format(x*1e-6)


def prepare_data_for_chart(movies_df, start_year, end_year):
    """
    Prepare movies data for visualization by aggregating average revenue and budget per year.
    Args:
    Args:
    movies_df (pd.DataFrame): A DataFrame containing the movies data.
    start_year (int): The start year for the data to visualize.
    end_year (int): The end year for the data to visualize.

    Returns:
    pd.DataFrame: A DataFrame ready for visualization.
    """
    if movies_df is None:
        print("Movies DataFrame is None.")
        return None
    movies_df = get_movies_year_range(movies_df, start_year, end_year)
    # Dodaj kolumnę release_year
    movies_df['release_year'] = movies_df['release_date'].dt.year
    movies_df = movies_df.groupby('release_year').agg({
        'revenue': 'mean',
        'budget': 'mean'
    }).reset_index()

    # Select relevant columns
    viz_df = movies_df[['release_year', 'revenue', 'budget']]

    return viz_df.reset_index(drop=True)


def create_chart(movies_df, start_year, end_year):
    """
    Create a line chart visualizing average revenue and budget over years.

    Args:
    viz_df (pd.DataFrame): A DataFrame containing the data for visualization.

    Returns:
    None
    """
    viz_df = prepare_data_for_chart(movies_df, start_year, end_year)
    if viz_df is None:
        print("Visualization DataFrame is None.")
        return

    fig, ax = plt.subplots()
    ax.plot(viz_df['release_date'], viz_df['budget'],
            label='Budżet', color='red')
    formatter = plt.FuncFormatter(million)
    ax.yaxis.set_major_formatter(formatter)
    ax.bar(viz_df['release_date'], viz_df['revenue'],
           color='blue', label='Przychód')
    ax.set_xticks(viz_df['release_date'])
    ax.set_title(
        f'Średni przychód i budżet filmu w latach {start_year}-{end_year}')

    plt.grid(False)
    plt.subplots_adjust(right=0.75)
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))  # Outside of plot
    plt.show()

# map genre_id in movies_df to genres in genres_df


def join_genres(movies_df, genres_df):
    genres_df = genres_df[['genres']]
    return movies_df.join(genres_df, on='genre_id', how='inner').rename(columns={'genres': 'genre'})


def get_top_genre(movies_df):
    if movies_df is None:
        print("Movies DataFrame is None.")
        return None
    top_genre = [movies_df['genre'].value_counts().idxmax(),
                 movies_df['genre'].value_counts().max()]
    return top_genre


def get_longest_average_runtime_genre(movies_df):
    if movies_df is None:
        print("Movies DataFrame is None.")
        return None
    average_runtime_by_genre = movies_df.groupby('genre')['runtime'].mean()
    longest_runtime_genre = average_runtime_by_genre.idxmax()
    return longest_runtime_genre


def create_genre_runtime_histogram(movies_df, genre_name):
    if movies_df is None:
        print("Movies DataFrame is None.")
        return None
    genre_movies = movies_df[movies_df['genre'] == genre_name]

    plt.hist(genre_movies['runtime'], bins=10, color='blue', edgecolor='black')
    plt.title(
        f'Histogram średniego czasu trwania filmów gatunku: {genre_name}')
    plt.xlabel('Czas trwania (minuty)')
    plt.ylabel('Liczba filmów')
    plt.grid(axis='y', alpha=0.75)
    plt.show()
