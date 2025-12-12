#%%
import numpy
import requests
from bs4 import BeautifulSoup
import pandas as pd
#
# url = 'https://en-wikipedia-org.translate.goog/wiki/List_of_largest_financial_services_companies_by_revenue?_x_tr_sl=en&_x_tr_tl=tr&_x_tr_hl=tr&_x_tr_pto=tc'
html_doc = """
<html>
  <body>
    <h1>Ürün Listesi</h1>
    <div class="product">
      <h2 class="title">Laptop</h2>
      <span class="price">1200</span>
    </div>
    <div class="product">
      <h2 class="title">Mouse</h2>
      <span class="price">150</span>
      <a class"___" href="emreer.com.tr">Emre Er </a>
    </div>
  </body>
</html>
"""

soup = BeautifulSoup(html_doc, 'html.parser')
# soup.find(tag, ...) → ilk bulduğu eleman
# soup.find_all(tag, ...) → tüm eşleşenler (liste)
# soup.select(css_selector) → CSS selector ile seçim

soup.find('h1') # urun listesi
h2_title = []
soup.find_all('h2') # tum h2 ler liste halinde
# for t in soup.find_all('h2'):
#     h2_title.append(t)
# h2_title
soup.find_all('div',class_= 'product')
price = soup.select('div.product span.price') # liste sekinde pricelar
price


# %%
tag = soup.find('h2', class_='title')

# 1) İç metin
text1 = tag.text
text1 # => 'laptop'
text2 = tag.get_text(strip=True)
text2 # => 'Laptop'

# 2) Attribute (ör: <a href="...">)

a_href = soup.find('a')

a_tag = a_href['href']
a_tag

# %%


from bs4 import BeautifulSoup
import pandas as pd
html_doc = """
<html>
  <body>
    <h1>Ürün Listesi</h1>

    <div class="product">
      <h2 class="title">Laptop</h2>
      <span class="price">1200</span>
      <span class="currency">TL</span>
    </div>

    <div class="product">
      <h2 class="title">Mouse</h2>
      <span class="price">150</span>
      <span class="currency">TL</span>
    </div>

    <div class="product">
      <h2 class="title">Klavye</h2>
      <span class="price">300</span>
      <span class="currency">TL</span>
    </div>

  </body>
</html>
"""

soup = BeautifulSoup(html_doc,'html.parser')

product_gives = soup.find_all('div', class_='product')

item_rows = []

for p in product_gives:
    title_tag = p.find('h2', class_='title')
    price_tag = p.find('span', class_='price')
    curre_tag = p.find('span', class_='currency')

    title = title_tag.get_text(strip=True) if title_tag else None
    price_text = price_tag.get_text(strip= True) if price_tag else None
    curren = curre_tag.get_text(strip= True) if curre_tag else None

    try:
        price = int(price_text)
    except (TypeError, ValueError):
        price = None

    item_rows.append({
        "product_name" : title,
        "price" : price,
        "currency" : curren
    })
    print("before ", type(price_text)) # string
    print("after ", type(price)) # int
item_rows

df = pd.DataFrame(item_rows)
df

df.to_csv('products.csv', index=False)


# %%
html_books = """
<html>
  <body>
    <h1>En Popüler Kitaplar</h1>

    <div class="book">
      <span class="title">Sefiller</span>
      <span class="author">Victor Hugo</span>
      <span class="rating">4.8</span>
    </div>

    <div class="book">
      <span class="title">Suç ve Ceza</span>
      <span class="author">Fyodor Dostoyevski</span>
      <span class="rating">4.7</span>
    </div>

    <div class="book">
      <span class="title">1984</span>
      <span class="author">George Orwell</span>
      <span class="rating">4.6</span>
    </div>

  </body>
</html>
"""

soup = BeautifulSoup(html_books, 'html.parser')
# Kitap adını, yazarı, puanını çekmek
# Bunları pandas DataFrame’e koymak

book_gives = soup.find_all('div', class_='book')
books = []
for book in book_gives:
    title_tag = book.find('span',class_= 'title')
    author_Tag = book.find('span', class_='author')
    rating_tag = book.find('span', class_='rating')

    title = title_tag.get_text(strip=False) if title_tag else numpy.nan
    author = author_Tag.get_text(strip=False) if author_Tag else numpy.nan
    rating_text = rating_tag.get_text(strip=False) if rating_tag else numpy.nan

    try:
        rating = float(rating_text)
    except(ValueError,TypeError):
        rating = None

    books.append({
        "title" : title,
        "author" : author,
        "Rating" : rating
    })

books

book_df = pd.DataFrame(books)

book_df.loc[1, 'title':'author']

book_df.to_csv('booksler.csv',index=False) # yanda ki 0 1 2 leri gonderir index


#%%
html_movies = """
<html>
  <body>
    <h1>Film Listesi</h1>

    <div class="movie" data-genre="Drama">
      <span class="title">The Godfather</span>
      <span class="year">1972</span>
      <span class="rating">9.2</span>
    </div>

    <div class="movie" data-genre="Sci-Fi">
      <span class="title">Interstellar</span>
      <span class="year">2014</span>
      <span class="rating">8.6</span>
    </div>

    <div class="movie" data-genre="Drama">
      <span class="title">Fight Club</span>
      <span class="year">1999</span>
      <span class="rating">8.8</span>
    </div>

    <div class="movie" data-genre="Animation">
      <span class="title">Spirited Away</span>
      <span class="year">2001</span>
      <span class="rating">8.5</span>
    </div>

  </body>
</html>
"""

soup = BeautifulSoup(html_movies,'html.parser')

movies = soup.find_all('div',class_='movie')
movies_list = []

for movie in movies:
    title_tag = movie.find('span',class_='title')
    year_tag = movie.find('span',class_='year')
    rating_tag = movie.find('span',class_='rating')
    genre = movie.attrs['data-genre']


    title = title_tag.get_text(strip=True) if title_tag else None
    year_text = year_tag.get_text(strip=True) if year_tag else None
    rating_text = rating_tag.get_text(strip=True) if rating_tag else None

    try:
        year = int(year_text)
        rating = float(rating_text)
    except(ValueError,TypeError):
        year = None
        rating = None

    movies_list.append({
        "title" : title,
        "year" : year,
        "rating" : rating,
        "genre" : genre
    })

movies_list

df = pd.DataFrame(movies_list)


df.to_csv('movies.csv', index=False)





