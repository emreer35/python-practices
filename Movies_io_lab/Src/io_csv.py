"""
Görev 1.1 – CSV oku (typing + validation)
data/movies.csv dosyası oluştur.
En az 10 satır olsun.
tags alanını CSV’de classic;oscar gibi “;” ile tut.
İstediğim fonksiyonlar:
read_movies_csv(path) -> list[dict]
year, rating, votes, id tip dönüşümü yap.
watched: "true"/"false" gibi değerlerden bool’a çevir.
tags: string → list[str]
validate_movie(movie) -> list[str]
Hata listesi döndürsün (rating 0–10 arası, year 1888–şimdi, title boş olmasın vb.)
Görev 1.2 – CSV yaz
write_movies_csv(path, movies):
Header’ı sabit yaz.
tags list → ; join.
watched bool → "true"/"false".
Zorlama: Yazdıktan sonra tekrar okuyup iki listenin “eşdeğer” olduğunu kontrol et.
"""
#%%
from datetime import datetime
import pandas as pd
in_path = '/Users/emreer/Desktop/Python Practices/Movies_io_lab/Data/movies.csv'
out_path = '/Users/emreer/Desktop/Python Practices/Movies_io_lab/Data/movies_out.csv'

import csv

def read_movies_csv(path):
    movies = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # boş satır / eksik başlık kontrolü
            if not row or not (row.get("id") and row.get("title")):
                continue

            watched_raw = (row.get("watched") or "").strip().lower()
            tags_raw = (row.get("tags") or "").strip()

            movie = {
                "id": int(row["id"]),
                "title": row["title"].strip(),
                "year": int(row["year"]),
                "genre": row["genre"].strip(),
                "rating": float(row["rating"]),
                "votes": int(row["votes"]),
                "watched": watched_raw in ("true", "1", "yes", "y"),
                "tags": [t.strip() for t in tags_raw.split(";") if t.strip()],
                "created_at": (row.get("created_at") or "").strip(),
            }
            movies.append(movie)

    return movies
"""
def read_movies_csv(path):
    movies = []
    with open(path,'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            id,title,year,genre,rating,votes,watched,tags,created_at = line.split(',')

            movie = {
                "id":int(id),
                "title":title,
                "year":int(year),
                "genre":genre,
                "rating":float(rating),
                "votes": int(votes),
                "watched": watched.strip().lower() in ("true","1","yes","y"),
                "tags" : [t.strip() for t in tags.split(';') if t.strip()],
                "created_at" : created_at
            }
            movies.append(movie)

    return movies
"""
def validate_movie(movie):
    errors = []

    if not isinstance(movie.get('id'), int) and movie['id'] < 0:
        errors.append("id must be a positive integer")

    title = (movie.get("title") or "").strip()
    if not title:
        errors.append("title cannot be empty")

    year = movie.get('year')
    current_year = datetime.now().year
    if not isinstance(year,int) or not (1880<= year<= current_year):
        errors.append("year must be between 1888 and {current_year}")

    rating = movie.get("rating")
    if not isinstance(rating,(int,float)) or not (0.00 <= float(rating) <= 10.00):
        errors.append("rating must be between 0.0 and 10.0")

    votes = movie.get("votes")
    if not isinstance(votes,int) or not votes < 0:
        errors.append("votes must be an integer and >= 0")

    genre = (movie.get("genre") or "").strip()
    if not genre:
        errors.append("genre cannot be empty")

    watched = movie.get('watched')
    if not isinstance(watched,bool):
        errors.append("watched must be boolean")

    tags = movie.get("tags")
    if not isinstance(tags,list):
        errors.append("tags must be a list of strings")

    created_at = (movie.get("created_at") or "").strip()
    if not created_at:
        errors.append("created_at cannot be empty")

    return errors

header = ["id","title","year","genre","rating","votes","watched","tags","created_at"]
def write_movies_csv(path,movies):
    df = pd.DataFrame(movies)

    df = df[header]

    df.to_csv(path, index=False, encoding="utf-8")




# movies = read_movies_csv(path)
# print(movies[0]["watched"], type(movies[0]["watched"]))
# print(movies[0]["tags"], type(movies[0]["tags"]))

# validate_movie(movies)
movies = read_movies_csv(in_path)
write_movies_csv(out_path, movies)
roundtrip = read_movies_csv(out_path)


