import requests
import csv
from datetime import datetime, timedelta


class MovieDataPreparation:
    def __init__(self, num_pages):
        self.num_pages = num_pages
        self.base_url = 'https://api.themoviedb.org/3'
        self.headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8'
        }

    def make_request(self, url):
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_movie_data(self, page):
        url = f'{self.base_url}/discover/movie?include_adult=false&include_video=false&sort_by=popularity.desc&page={page}'
        data = self.make_request(url)
        return data.get('results', [])

    def get_genre_data(self):
        url = f'{self.base_url}/genre/movie/list?language=en'
        data = self.make_request(url)
        return data.get('genres', [])

    def get_sample_data(self):
        movies = []
        for page in range(1, self.num_pages + 1):
            movies.extend(self.get_movie_data(page))
        return movies

    def get_movies_with_indexes(self):
        movies = self.get_sample_data()
        return movies[3:20:4]

    def get_most_popular_title(self):
        movies = self.get_sample_data()
        movies.sort(key=lambda movie: movie.get('popularity', 0), reverse=True)
        return movies[0].get('title', '')

    def get_movies_with_keywords(self, keywords):
        movies = self.get_sample_data()
        result = []
        for movie in movies:
            if any(keyword.lower() in movie.get('overview', '').lower() for keyword in keywords):
                result.append(movie.get('title', ''))
        return result

    def get_unique_genres(self):
        genres = self.get_genre_data()
        unique_genres = set(genre['name'] for genre in genres)
        return unique_genres

    def remove_movies_by_genre(self, genre):
        movies = self.get_sample_data()
        genre_ids_to_remove = []

        genres = self.get_genre_data()
        for g in genres:
            if g['name'].lower() == genre.lower():
                genre_ids_to_remove.append(g['id'])

        filtered_movies = [movie for movie in movies if
                           not any(genre_id in genre_ids_to_remove for genre_id in movie.get('genre_ids', []))]

        return filtered_movies

    def get_popular_genre_counts(self):
        movies = self.get_sample_data()
        genre_counts = {}
        for movie in movies:
            genre_ids = movie.get('genre_ids', [])
            for genre_id in genre_ids:
                genre_counts[genre_id] = genre_counts.get(genre_id, 0) + 1

        genres = self.get_genre_data()
        popular_genres = []
        for genre in genres:
            genre_id = genre.get('id')
            genre_name = genre.get('name')
            if genre_id in genre_counts:
                popular_genres.append((genre_name, genre_counts[genre_id]))
        popular_genres.sort(key=lambda x: x[1], reverse=True)
        return popular_genres

    def get_movies_grouped_by_genre(self):
        movies = self.get_sample_data()
        genres = self.get_genre_data()
        genre_movies = {genre['id']: [] for genre in genres}

        for movie in movies:
            genre_ids = movie.get('genre_ids', [])
            for genre_id in genre_ids:
                genre_movies[genre_id].append(movie.get('title', ''))

        result = []
        for genre_id, movies in genre_movies.items():
            if len(movies) > 1:
                result.append((genre_id, movies))
        return result

    def modify_genre_ids(self):
        movies = self.get_sample_data()
        modified_movies = []

        for movie in movies:
            modified_movie = movie.copy()
            genre_ids = modified_movie.get('genre_ids')
            if genre_ids:
                modified_movie['genre_ids'] = [22] + genre_ids[1:]
            modified_movies.append(modified_movie)

        return movies, modified_movies

    def get_movies_info(self):
        movies = self.get_sample_data()
        movies_info = []

        for movie in movies:
            title = movie.get('title', '')
            popularity = round(movie.get('popularity', 0), 1)
            vote_average = int(movie.get('vote_average', 0))
            release_date = datetime.strptime(movie.get('release_date', ""), '%Y-%m-%d')
            last_day_in_cinema = release_date + timedelta(weeks=14)
            last_day_in_cinema += timedelta(days=(6 - last_day_in_cinema.weekday()) % 7)

            movie_info = {
                'title': title,
                'popularity': popularity,
                'vote_average': vote_average,
                'last_day_in_cinema': last_day_in_cinema.strftime('%Y-%m-%d')
            }
            movies_info.append(movie_info)

        movies_info.sort(key=lambda x: (x['vote_average'], x['popularity']), reverse=True)
        return movies_info

    def save_movies_info_to_csv(self, filepath):
        movies_info = self.get_movies_info()
        fieldnames = list(movies_info[0].keys())

        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(movies_info)


num_pages = 5

movie_data = MovieDataPreparation(num_pages)

sample_data = movie_data.get_sample_data()
print('Sample data:')
print(sample_data)
print()

movies_indexes = movie_data.get_movies_with_indexes()
print('Movies with indexes 3 to 19 with a step of 4:')
print(movies_indexes)
print()

most_popular_title = movie_data.get_most_popular_title()
print('Most popular title:')
print(most_popular_title)
print()

keywords = ['action', 'adventure']
movies_with_keywords = movie_data.get_movies_with_keywords(keywords)
print(f'Movies with keywords {keywords}:')
print(movies_with_keywords)
print()

unique_genres = movie_data.get_unique_genres()
print('Unique genres:')
print(unique_genres)
print()

genre_to_remove = 'Drama'
filtered_movies = movie_data.remove_movies_by_genre(genre_to_remove)
print(f'Movies after removing the genre "{genre_to_remove}":')
print(filtered_movies)
print()

popular_genre_counts = movie_data.get_popular_genre_counts()
print('Popular genres with their occurrence counts:')
print(popular_genre_counts)
print()

movies_grouped_by_genre = movie_data.get_movies_grouped_by_genre()
print('Movies grouped by genre:')
print(movies_grouped_by_genre)
print()

movies, modified_movies = movie_data.modify_genre_ids()
print('Original movies:')
print(movies)
print('Modified movies with genre ID replaced:')
print(modified_movies)
print()

movies_info = movie_data.get_movies_info()
print('Movies info:')
print(movies_info)
print()

csv_filepath = 'movies_info.csv'
movie_data.save_movies_info_to_csv(csv_filepath)
print(f'Movies info saved to "{csv_filepath}" as a CSV file.')
