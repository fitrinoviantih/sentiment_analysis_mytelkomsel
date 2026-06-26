# 1. Install for scraper's library from Google Play and Pandas
# pip install google-play-scraper
# pip install pandas

# 2. Import the library
from google_play_scraper import app
import pandas as pd 

# 3. Scraping process
# based on the 1000 newest reviews, from Indonesian, and Indonesia language, without any filter scores 
from google_play_scraper import Sort, reviews

result, continuation_token = reviews(
    'com.telkomsel.telkomselcm',
    lang='id',
    country='id',
    sort=Sort.NEWEST,
    count=1000,
    filter_score_with=None,
)
print(f"Data yang berhasil ditarik: {len(result)} ulasan")

# 4. Display scraping result (showing the top 5 rows)
df_busu = pd.DataFrame(result)
df_busu[['userName', 'score', 'at', 'content']]
print(df_busu.head())

# 5. Display the number of scraping data records 
len (df_busu.index)

# 6. Save the result of scraping in 4 rows
my_df_scrape = df_busu[['userName', 'score', 'at', 'content']]

# 7. Save the data result's as Excel file
my_df_scrape.to_excel('RAW_data_review_mytelkomsel.xlsx', index=False)