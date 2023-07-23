import requests
import csv
from datetime import datetime, timedelta
from collections import Counter


class MovieDataPreparation:
    def __init__(self, num_pages):
        self.num_pages = num_pages
        self.base_url = 'https://api.themoviedb.org/3'
        self.headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMTI3NGFmYTRlNTUyMjRjYzRlN2Q0NmNlMTNkOTZjOSIsInN1YiI6IjVkNmZhMWZmNzdjMDFmMDAxMDU5NzQ4OSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.lbpgyXlOXwrbY0mUmP-zQpNAMCw_h-oaudAJB6Cn5c8'
        }
        self.movies = self.get_sample_data()
        self.genres = self.get_genre_data()

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

    def get_all_data(self):
        return self.movies

    def get_movies_with_indexes(self):
        movies = self.get_sample_data()
        return movies[3:20:4]

    def get_most_popular_title(self):
        return max(self.movies, key=lambda movie: movie.get('popularity', 0)).get('title', '')

    def get_movies_with_keywords(self, keywords):
        return [movie.get('title', '') for movie in self.movies if
                any(keyword.lower() in movie.get('overview', '').lower() for keyword in keywords)]

    def get_unique_genres(self):
        return set(genre['name'] for genre in self.genres)

    def remove_movies_by_genre(self, genre):
        genre_ids_to_remove = [g['id'] for g in self.genres if g['name'].lower() == genre.lower()]

        return [movie for movie in self.movies if
                not any(genre_id in genre_ids_to_remove for genre_id in movie.get('genre_ids', []))]

    def get_popular_genre_counts(self):
        genre_counts = Counter()
        for movie in self.movies:
            genre_ids = movie.get('genre_ids', [])
            genre_counts.update(genre_ids)

        popular_genres = [(genre['name'], count) for genre in self.genres for genre_id, count in genre_counts.items() if
                          genre.get('id') == genre_id]
        popular_genres.sort(key=lambda x: x[1], reverse=True)
        return popular_genres

    def get_movies_grouped_by_genre(self):
        genre_movies = {genre['id']: [] for genre in self.genres}

        for movie in self.movies:
            genre_ids = movie.get('genre_ids', [])
            for genre_id in genre_ids:
                genre_movies[genre_id].append(movie.get('title', ''))

        return list(filter(lambda genre_info: len(genre_info[1]) > 1, genre_movies.items()))

    def modify_genre_ids(self):
        def modify_movie_genre_ids(movie):
            modified_movie = movie.copy()
            genre_ids = modified_movie.get('genre_ids')
            if genre_ids:
                modified_movie['genre_ids'] = [22] + genre_ids[1:]
            return modified_movie

        modified_movies = list(map(modify_movie_genre_ids, self.movies))

        return self.movies, modified_movies

    def get_movie_info(self):
        movies_info = []
        for movie in self.movies:
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
        return movies_info

    def get_movies_info(self):
        movies_info = self.get_movie_info()
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

sample_data = movie_data.get_all_data()
print('Sample data:')
print(sample_data, end='\n\n')

movies_indexes = movie_data.get_movies_with_indexes()
print('Movies with indexes 3 to 19 with a step of 4:')
print(movies_indexes, end='\n\n')

most_popular_title = movie_data.get_most_popular_title()
print('Most popular title:')
print(most_popular_title, end='\n\n')

keywords = ['action', 'adventure']
movies_with_keywords = movie_data.get_movies_with_keywords(keywords)
print(f'Movies with keywords {keywords}:')
print(movies_with_keywords, end='\n\n')

unique_genres = movie_data.get_unique_genres()
print('Unique genres:')
print(unique_genres, end='\n\n')

genre_to_remove = 'Drama'
filtered_movies = movie_data.remove_movies_by_genre(genre_to_remove)
print(f'Movies after removing the genre "{genre_to_remove}":')
print(filtered_movies, end='\n\n')

popular_genre_counts = movie_data.get_popular_genre_counts()
print('Popular genres with their occurrence counts:')
print(popular_genre_counts, end='\n\n')

movies_grouped_by_genre = movie_data.get_movies_grouped_by_genre()
print('Movies grouped by genre:')
print(movies_grouped_by_genre, end='\n\n')

movies, modified_movies = movie_data.modify_genre_ids()
print('Original movies:')
print(movies)
print('Modified movies with genre ID replaced:')
print(modified_movies, end='\n\n')

movies_info = movie_data.get_movies_info()
print('Movies info:')
print(movies_info, end='\n\n')

csv_filepath = 'movies_info.csv'
movie_data.save_movies_info_to_csv(csv_filepath)
print(f'Movies info saved to "{csv_filepath}" as a CSV file.')
