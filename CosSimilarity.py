import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re



# LOADING DATA
data1 = pd.read_excel(r"C:\ma projects\productMatcher\dataFiles\data1.xlsx", header=None, names=["Product"])
data2 = pd.read_excel(r"C:\ma projects\productMatcher\dataFiles\data2.xlsx", header=None, names=["Product"])



# DATA CLEANING, PREPROCESSING & NORMALIZATION
persian_to_english = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")      # DIGIT MAPPING (FARSI TO ENGLISH)
stopwords = {"ماشین","اصل" ,"orginal"}                              # REMOVING GENERAL UNINFORMATIVE WORDS

def preprocess(text):

    text = text.strip().lower()                                    # STRIP WHITESPACE & CONVERT TO lowercase

    text = text.translate(persian_to_english)                      # NORMALIZE FARSI DIGITS

    for word in stopwords:                                         # REMOVE STOPWORDS
        text = text.replace(word, "")
    return re.sub(r'\s+', ' ', text).strip()           # REMOVE EXTRA SPACES

data1["Product"] = data1["Product"].apply(preprocess)
data2["Product"] = data2["Product"].apply(preprocess)
print("Data After Preprocessing", "\n", "data1", data1.head(), "\n", "\n", "data2", data2.head(), "\n",)




# COSINE SIMILARITY

all_products = pd.concat([data1["Product"], data2["Product"]], ignore_index=True)    # Combining all product names for vectorization

# PRODUCT NAMES TO TF-IDF VECTORS
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(all_products)

similarity_matrix = cosine_similarity(tfidf_matrix)                 # COSINE SIMILARITY MATRIX

num_data1 = len(data1)                                              # EXTRAT RELEVANT PARTS
cosine_similarities = similarity_matrix[:num_data1, num_data1:]     # ONLY COMPARISONS BETWEEN data1 & data2

threshold = 0.6

# FINING PAIRS ABOVE THRESHOLD
matches = []
for i, row in enumerate(cosine_similarities):
    best_match_index = row.argmax()
    similarity_score = row[best_match_index]

    if similarity_score >= threshold:
        matches.append((data1.iloc[i, 0], data2.iloc[best_match_index, 0], similarity_score))

# DISPLAY RESULTS
for product1, product2, score in matches:
    print(f"Cosine Match: '{product1}' ↔ '{product2}' (Score: {score:.2f})")

# SAVING RESULTS AS EXCEL FILE
output_df = pd.DataFrame(matches, columns=["Product 1", "Product 2", "Similarity Score"])
output_df.to_excel(r"C:\ma projects\productMatcher\cosine_matches.xlsx", index=False)
print("✅ Cosine matches saved to cosine_matches.xlsx")