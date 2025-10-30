import utils


def main():

    movies_df = utils.load_movies_data()

    # 1 Lista najwyżej ocenianych filmów
    top_rated_movies = utils.get_top_rated_movies(movies_df, top_n=10)

    utils.create_chart(movies_df, 2010, 2016)


if __name__ == "__main__":
    main()
