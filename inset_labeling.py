# 1. Install the InSet reporitory from: https://github.com/fajri91/InSet

# 2. Import the Pandas library
import pandas as pd

# 3. Load the lexicon InSet
pos_dict = pd.read_csv(r"/content/positive.tsv", sep='\t', names=['word', 'score'])
neg_dict = pd.read_csv(r"/content/negative.tsv", sep='\t', names=['word', 'score'])

# 4. Load the Excel file
df = pd.read_excel(r"content/data_setelah_preprocessing_mytelkomsel.xlsx")

# 5. Convert the score to a number (preventing a TypeError)
pos_dict['score'] = pd.to_numeric(pos_dict['score'], errors='coerce').fillna(0)
neg_dict['score'] = pd.to_numeric(neg_dict['score'], errors='coerce').fillna(0)

word_dict = dict(zip(pos_dict['word'], pos_dict['score']))
word_dict.update(dict(zip(neg_dict['word'], neg_dict['score'])))

# 6. Drop the missing values
df.dropna(subset=['hasil_akhir_preprocessing'], inplace=True)
df = df[df['hasil_akhir_preprocessing'].astype(str).str.strip() != ""]

# 7. Function for pick the scores and labels 
def get_lexicon_label(text):
    score = 0
    words = str(text).lower().split()
    for word in words:
        if word in word_dict:
            score += word_dict[word]

    # Labeling process (2 classes: positive and negative)
    LABEL = 'POSITIF' if score > 0 else 'NEGATIF'
    return pd.Series([score, LABEL]) 

df[['lexicon_score', 'label']] = df['hasil_akhir_preprocessing'].apply(get_lexicon_label)

# 8. Show the results and total data
print("\n" + "="*25)
print("RESULT OF LEXICON LABELING")
print("="*25)
print(df['label'].value_counts())
print("-"*25)
print(f"Total Data: {len(df)}")
print("="*25)

# 9. Save the result as Excel file
df.to_excel(r"/content/lexicon_label_untuk_modeling.xlsx", index=False)