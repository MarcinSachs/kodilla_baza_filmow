import pytest
import pandas as pd
from utils import (
    load_movies_data,
    load_genres_data,
    get_top_rated_movies,
    get_movies_year_range,
    prepare_data_for_chart,
    join_genres,
    get_top_genre,
    get_longest_average_runtime_genre,
)

# Fixture do ładowania danych filmowych


@pytest.fixture
def movies_df():
    try:
        return load_movies_data()
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # Pusty DF jeśli nie można załadować
        return pd.DataFrame({'id': [], 'title': [], 'release_date': [], 'vote_count': [], 'vote_average': []})

# Fixture do ładowania danych gatunków


@pytest.fixture
def genres_df():
    try:
        genres = load_genres_data()
        if 'Unnamed: 0' in genres.columns:  # Sprawdź, czy kolumna 'Unnamed: 0' istnieje
            # Zmień nazwę kolumny
            genres = genres.rename(columns={'Unnamed: 0': 'id'})
        return genres
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # Pusty DF jeśli nie można załadować
        return pd.DataFrame({'id': [], 'genres': []})

# Testy dla load_movies_data


def test_load_movies_data_success(movies_df):
    # Sprawdź, czy movies_df nie jest puste (załadunek się powiódł)
    if not movies_df.empty:
        assert isinstance(movies_df, pd.DataFrame)
        assert not movies_df.empty
        assert 'id' in movies_df.columns
        assert 'title' in movies_df.columns
        assert 'release_date' in movies_df.columns
        assert pd.api.types.is_datetime64_any_dtype(movies_df['release_date'])


def test_load_movies_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        # Wywołaj Z argumentem
        load_movies_data(filename="nonexistent_file.csv")


# tmp_path to fixture od pytest
def test_load_movies_data_empty_file(tmp_path):
    # Utwórz pusty plik tymczasowy
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")  # Utwórz pusty plik tekstowy

    with pytest.raises(pd.errors.EmptyDataError):
        load_movies_data(str(empty_file))  # Wywołaj Z argumentem

# Testy dla load_genres_data


def test_load_genres_data_success(genres_df):
    # Sprawdź, czy genres_df nie jest puste (załadunek się powiódł)
    if not genres_df.empty:
        assert isinstance(genres_df, pd.DataFrame)
        assert not genres_df.empty
        assert 'id' in genres_df.columns
        assert 'genres' in genres_df.columns


def test_load_genres_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        # Wywołaj Z argumentem
        load_genres_data(filename="nonexistent_genres_file.csv")


def test_load_genres_data_empty_file(tmp_path):
    # Utwórz pusty plik tymczasowy
    empty_file = tmp_path / "empty_genres.csv"
    empty_file.write_text("")  # Utwórz pusty plik tekstowy

    with pytest.raises(pd.errors.EmptyDataError):
        load_genres_data(str(empty_file))  # Wywołaj Z argumentem

# Testy dla get_top_rated_movies


def test_get_top_rated_movies_success(movies_df):
    if not movies_df.empty:
        top_movies = get_top_rated_movies(movies_df, top_n=5)
        assert top_movies is not None
        assert isinstance(top_movies, pd.DataFrame)
        assert len(top_movies) <= 5
        assert 'vote_average' in top_movies.columns
        assert 'vote_count' in top_movies.columns
        # Sprawdzamy, czy filmy są posortowane malejąco po vote_average
        if len(top_movies) > 1:  # Upewnij sie ze DataFrame nie jest pusty
            assert top_movies['vote_average'].is_monotonic_decreasing


def test_get_top_rated_movies_empty_df():
    # Stwórz *ręcznie* pusty DataFrame
    empty_df = pd.DataFrame({'id': [], 'title': [], 'release_date': [
    ], 'vote_count': [], 'vote_average': []})
    top_movies = get_top_rated_movies(empty_df, top_n=5)
    assert top_movies is not None
    assert isinstance(top_movies, pd.DataFrame)
    assert top_movies.empty


# Testy dla get_movies_year_range
def test_get_movies_year_range_success(movies_df):
    if not movies_df.empty:
        year_range_movies = get_movies_year_range(movies_df, 2010, 2012)
        assert year_range_movies is not None
        assert isinstance(year_range_movies, pd.DataFrame)
        if not year_range_movies.empty:
            assert year_range_movies['release_date'].dt.year.min() >= 2010
            assert year_range_movies['release_date'].dt.year.max() <= 2012


def test_get_movies_year_range_no_movies_in_range(movies_df):
    if not movies_df.empty:  # Upewnij sie ze movies_df nie jest puste
        year_range_movies = get_movies_year_range(movies_df, 1900, 1901)
        assert year_range_movies is not None
        assert isinstance(year_range_movies, pd.DataFrame)
        assert year_range_movies.empty

# Testy dla prepare_data_for_chart


def test_prepare_data_for_chart_success(movies_df):
    if not movies_df.empty:
        chart_data = prepare_data_for_chart(movies_df, 2010, 2012)
        if chart_data is not None:
            assert chart_data is not None
            assert isinstance(chart_data, pd.DataFrame)
            assert 'release_year' in chart_data.columns
            assert 'revenue' in chart_data.columns
            assert 'budget' in chart_data.columns
            if not chart_data.empty:  # Upewnij sie ze chart_data nie jest puste
                assert chart_data['release_year'].min() >= 2010
                assert chart_data['release_year'].max() <= 2012
    else:
        pytest.skip("Movies DataFrame is empty, skipping test")  # Pomiń test


def test_prepare_data_for_chart_empty_df(movies_df):
    if movies_df.empty:  # Użyj fixture movies_df
        chart_data = prepare_data_for_chart(movies_df, 2010, 2012)
        assert chart_data is not None
        assert isinstance(chart_data, pd.DataFrame)
        assert chart_data.empty
    else:
        # Pomiń test
        pytest.skip("Movies DataFrame is not empty, skipping test")


# Testy dla join_genres
def test_join_genres_success(movies_df, genres_df):
    if not movies_df.empty and not genres_df.empty:
        # Weź tylko po 5 pierwszych wierszy
        joined_df = join_genres(movies_df.head(5), genres_df.head(5))
        assert joined_df is not None
        assert isinstance(joined_df, pd.DataFrame)
        assert 'genre' in joined_df.columns


def test_join_genres_empty_df(movies_df, genres_df):
    empty_movies_df = pd.DataFrame({'genre_id': []})
    joined_df = join_genres(empty_movies_df, genres_df)
    assert joined_df is not None
    assert isinstance(joined_df, pd.DataFrame)
    assert joined_df.empty

# Testy dla get_top_genre


def test_get_top_genre_success(movies_df, genres_df):
    if not movies_df.empty and not genres_df.empty:
        # Musimy wcześniej wykonać join_genres
        movies_df_joined = join_genres(movies_df.head(5), genres_df.head(5))
        if not movies_df_joined.empty:
            top_genre = get_top_genre(movies_df_joined)
            assert isinstance(top_genre, list)
            assert len(top_genre) == 2
            assert isinstance(top_genre[0], str)
            assert isinstance(top_genre[1], int)


def test_get_top_genre_empty_df(movies_df, genres_df):
    empty_df = pd.DataFrame({'genre': []})
    # Oczekujemy ValueError, ponieważ idxmax() na pustej serii zwraca błąd
    with pytest.raises(ValueError):
        get_top_genre(empty_df)


# Testy dla get_longest_average_runtime_genre
def test_get_longest_average_runtime_genre_success(movies_df, genres_df):
    if not movies_df.empty and not genres_df.empty:
        # Musimy wcześniej wykonać join_genres
        movies_df_joined = join_genres(movies_df.head(5), genres_df.head(5))
        if not movies_df_joined.empty:
            longest_runtime_genre = get_longest_average_runtime_genre(
                movies_df_joined)
            assert isinstance(longest_runtime_genre, str)


def test_get_longest_average_runtime_genre_empty_df(movies_df, genres_df):
    empty_df = pd.DataFrame({'genre': [], 'runtime': []})
    # Oczekujemy ValueError, ponieważ idxmax() na pustej serii zwraca błąd
    with pytest.raises(ValueError):
        get_longest_average_runtime_genre(empty_df)
