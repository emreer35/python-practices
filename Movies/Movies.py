
"""
Yapılacaklar (Task List)
load_movies(path) -> list[dict]
rating float, year int olacak
filter_movies(movies, min_year=2000) -> list[dict]
sort_movies(movies): year artan, rating azalan
summary_by_genre(movies) -> dict
her genre için: count, avg_rating, best_title
Sonuçları report.txt ve report.json olarak kaydet
“Teslim formatı”
main.py (çalıştırınca raporu üretsin)
movies.csv (10–30 satır yeter)
"""


from matplotlib.pyplot import title

"""
Aşağıdaki iki fonksiyonu yazıp buraya yapıştır:
load_movies(path)
open(path) ile oku
header satırını atla
boş satır varsa geç
title string, year int, genre string, rating float
summary_by_genre(movies)
çıktı şöyle bir dict olsun:
"""
#%%
import json
path = '/Users/emreer/Desktop/Python Practices/Movies/movies.csv'
def load_movies(path):
    movies = []
    with open(path,'r') as file:
        lines = file.readlines()
        header = lines[0]
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue
            title,year,genre,rating = line.split(',')
            movie = {
                "title" : title,
                "year" : int(year),
                "genre": genre,
                "rating" : float(rating)
            }

            movies.append(movie)
    return movies

def summary_by_genre(movies):
    summary = {}
    for m in movies:
        g = m["genre"]

        if g not in summary:
            summary[g] = {
                "count": 0,
                "sum_rating": 0.0,
                "best_rating": -1.0,
                "best_title": ""
            }

        summary[g]["count"] += 1
        summary[g]["sum_rating"] += m["rating"]

        if m["rating"] > summary[g]["best_rating"]:
            summary[g]["best_rating"] = m["rating"]
            summary[g]["best_title"] = m["title"]

    for g in summary:
        count = summary[g]["count"]
        summary[g]["avg_rating"] = summary[g]["sum_rating"] / count

        del summary[g]["sum_rating"]
        del summary[g]["best_rating"]

    return summary

def filter_by_year(movies, min_year=2000):
    return [m for m in movies if m["year"] > min_year]

def sort_movies(movies):
    return  sorted(movies, key=lambda m : (m['year'], -m['rating']))


def save_report_txt(report, filename="Movies/report.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for genre, info in report.items():
            f.write(
                f"{genre} | count={info['count']} | avg={info['avg_rating']:.2f} | best={info['best_title']}\n"
            )

def save_report_json(report, filename="Movies/report.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

movie = load_movies(path)
report = summary_by_genre(movie)

sort_movies(movie)
filter_by_year(movie)

save_report_txt(report)
save_report_json(report)

