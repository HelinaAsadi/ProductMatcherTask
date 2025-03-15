import pandas as pd
from rapidfuzz import fuzz, process
import itertools
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
print("Data After Preprocessing", "\n", "\n", "data1", data1.head(), "\n", "data2", data2.head(), "\n",)



#FUZZY
# PAIRING
def find_matches(data1, data2, threshold=30):
    matches = []
    for product in data1["Product"]:
        match, score, _ = process.extractOne(product, data2["Product"], scorer=fuzz.token_set_ratio)
        if score >= threshold:  # Only keep matches with similarity above the threshold
            matches.append((product, match, score))
    return matches

matches = find_matches(data1, data2)

# SAVING RESULTS OF GROUPING
match_df = pd.DataFrame(matches, columns=["Data1 Product", "Data2 Product", "Similarity Score"])
match_df.to_excel("fuzzy_paired_products.xlsx", index=False)
print("✅ Matches saved to fuzzy_paired_products.xlsx")



# FUZZY
# GROUPING
def group_similar_products(data1, data2, threshold=70):
    all_products = pd.concat([data1, data2], ignore_index=True)["Product"].unique()
    clusters = []

    while len(all_products) > 0:
        current = all_products[0]
        similar = process.extract(current, all_products, scorer=fuzz.token_set_ratio, score_cutoff=threshold)
        cluster = [item[0] for item in similar]
        clusters.append(cluster)
        all_products = [p for p in all_products if p not in cluster]

    return clusters

clusters = group_similar_products(data1, data2)

# SAVING RESULTS OF GROUPING
pd.DataFrame({"Group": [i + 1 for i, g in enumerate(clusters)], "Products": clusters}).to_excel("fuzzy_grouped_products.xlsx",
                                                                                                index=False)
print("✅ Grouped products saved to fuzzy_grouped_products.xlsx")