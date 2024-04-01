from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import time

# Downloading imdb top 250 movie's data
url = 'https://www.imdb.com/search/title/?groups=top_1000&count=100&sort=user_rating,asc'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print('Failed to fetch data:', response.status_code)
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Write the HTML content to a text file
with open('imdb_top_250_movies_html.txt', 'w', encoding='utf-8') as file:
    file.write(str(soup))
Title = []
Release_Year = []
IMDb_Rating =[]
Summary =[]
# Find all elements with a specific class

movie_name = soup.find_all('h3', class_='ipc-title__text')
Release_Year1 = soup.find_all('span', class_='sc-b0691f29-8 ilsLEX dli-title-metadata-item')
IMDb_Rating1 = soup.find_all('span',class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating')
Summary1 = soup.find_all('div',class_="ipc-html-content-inner-div")

# Convert ResultSet to a list
movie_name = list(movie_name)

# Remove the last element from the list
movie_name.pop()

for item in movie_name:
    # Extract relevant information from the item
    Title.append(item.text)
for idx, item in enumerate(Release_Year1):
    if idx % 3 == 0:
        Release_Year.append(item.text)
for item in IMDb_Rating1:
    split_data = item.text[0:3]
    IMDb_Rating.append(split_data)
for item in Summary1:
    Summary.append(item.text)

df = pd.DataFrame({
    'Title': Title,
    'Release_Year' :Release_Year,
    'IMDb_Rating':IMDb_Rating,
    'Summary': Summary
})
print("Df : ",df)
# Create a DataFrame and save it to a CSV file
df.to_csv('imdb_top_250_movies.csv', index=False)
