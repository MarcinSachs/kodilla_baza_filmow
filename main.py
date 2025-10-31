import utils


def main():

    movies_df = utils.load_movies_data()

    # 1 Lista najwyżej ocenianych filmów
    top_rated_movies = utils.get_top_rated_movies(movies_df, top_n=10)

    # 2 Wykres średniego budżetu i przychodu filmów w wybranym przedziale lat
    utils.create_chart(movies_df, 2010, 2016)

    # 3 Łączenie danych o gatunkach z danymi o filmach
    movies_df = utils.join_genres(movies_df, utils.load_genres_data())

    # 4 Najpopularniejszy gatunek filmowy
    top_genre = utils.get_top_genre(movies_df)
    print(
        f"Najpopularniejszy gatunek filmowy w bazie to: {top_genre[0]}. W bazie znajduje się {top_genre[1]} filmów tego gatunku.")

    # 5 Gatunek filmowy z najdłuższym średnim czasem trwania
    top_genre_runtime = utils.get_longest_average_runtime_genre(movies_df)
    print(
        f"Gatunek filmowy z najdłuższym średnim czasem trwania to: {top_genre_runtime}.")

    # 6 Histogram średniego czasu trwania filmów według gatunku
    utils.create_genre_runtime_histogram(movies_df, top_genre_runtime)


if __name__ == "__main__":
    main()
