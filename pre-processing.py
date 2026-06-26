# 1. Install Pandas, NLTK, and Sastrawi library 
# pip install pandas
# pip install nltk
# pip install Sastrawi

# 2. Import all of the library's
import pandas as pd

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# 3. Install the packages from NLTK library
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

# 4. Read the Excel file from the scraping process and shows the top 5 rows
df = pd.read_excel('review_mytelkomsel.xlsx')
df.head()

# 5. Case folding process, and shows the top 5 rows
df['casefolding'] = df['CONTENT'].astype(str).str.lower()
df.head()

# 6. Tokenizing process and shows the top 5 rows
df['tokenizing'] = df['casefolding'].apply(word_tokenize)
df['tokenizing'] = df['tokenizing'].apply(
    lambda tokens: [t for t in tokens if t.isalpha()]
)
df.head()

# 7. Filtering process using stopword removal and shows the top 5 rows
# using "kata_penting" for exception words
stopword_id = set(stopwords.words('indonesian'))

kata_penting = {
    'telkomsel',
    'baik',
    'buruk',
    'jelek',
    'bagus',
    'mantap',
    'oke',
    'ok',
    'lemot',
    'luar',
    'biasa',
    'tidak',
    'sangat',
    'cukup',
    'puas',
    'suka',
    'keren'
}

stopword_id = stopword_id - kata_penting

df['stopword'] = df['tokenizing'].apply(
    lambda x: [word for word in x if word not in stopword_id]
)

df.head()

# 8. Stemming process with whitelist some words and shows the top 5 rows 
factory = StemmerFactory()
stemmer = factory.create_stemmer()

kata_penting_2 = {
    'lemot',
    'jaringan',
    'error',
    'crash',
    'bug',
    'lag',
    'loading'
}

# normalize whitelist
kata_penting_2 = {w.lower().strip() for w in kata_penting_2}

def custom_stemming(tokens):
    result = []
    for w in tokens:
        w = w.lower().strip()
        if w in kata_penting_2:
          result.append(w)  
        else:
          result.append(stemmer.stem(w))
    return result

df.head()

# 9.Detokenizing process and shows the top 5 rows
df['stemming'] = df['stopword'].apply(custom_stemming)

df['hasil_akhir_preprocessing'] = df['stemming'].apply(lambda x: ' '.join(x))
df.head()

# 10. Export the data result in Excel file
df_export = df[['USERNAME', 'SCORE', 'AT', 'hasil_akhir_preprocessing']]
df_export.to_excel('result_preprocessing.xlsx', index=False)