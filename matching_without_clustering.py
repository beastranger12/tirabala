import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import fuzz, process

# Load the spaCy NLP model
nlp = spacy.load('en_core_web_md')

def preprocess(text):
    if not isinstance(text, str):
        return ''
    doc = nlp(text.lower())
    return ' '.join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

# Load data
nykaa = pd.read_csv('nykaa.csv')
tira = pd.read_csv('tira.csv')

print("Preprocessing data...")
nykaa['processed'] = nykaa['product_title'].apply(lambda x: preprocess(x))
tira['processed'] = tira['product_title'].apply(lambda x: preprocess(x))

print("Vectorizing data...")
vectorizer = TfidfVectorizer()
nykaa_vectors = vectorizer.fit_transform(nykaa['processed'])
tira_vectors = vectorizer.transform(tira['processed'])

print("Matching data using FuzzyWuzzy...")
matches = []
total_nykaa = len(nykaa)
for index, nykaa_row in nykaa.iterrows():
    progress = (index + 1) / total_nykaa * 100
    print(f"Processing item {index+1}/{total_nykaa}, {progress:.2f}% completed...")
    best_match, best_score = process.extractOne(nykaa_row['processed'], tira['processed'].tolist(), scorer=fuzz.token_sort_ratio)
    if best_score > 25:  # Threshold for matching can be adjusted based on desired accuracy
        tira_row = tira.iloc[tira['processed'].tolist().index(best_match)]
        matches.append({
            'Nykaa_ID': nykaa_row['id'],
            'Tira_ID': tira_row['id'],
            'Nykaa_Title': nykaa_row['product_title'],
            'Tira_Title': tira_row['product_title'],
            'Score': best_score
        })

matched_df = pd.DataFrame(matches)
matched_df.to_csv('matched_results_without_clustering.csv', index=False)
print("Matched results saved to 'matched_results_without_clustering.csv'.")
