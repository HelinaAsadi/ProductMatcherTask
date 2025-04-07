PRODUCT MATCHING
Task Report on Applied Approaches
Helina Asadi


Problem Analysis
Overview
Develop a Python algorithm to identify and group similar product names.
Data
2 .xlsx Excel files each including a total of 7 product names listed in a column
Challenges
Variations in product naming, word order, and language differences.

Data Preprocessing

LOAD DATA
Using pandas pd, read_data function, to load data as a list of Products.

Data Cleaning:

Stripping whitespace
Converting to lowercase
Digit mapping all Farsi digits to English
Removing uninformative and general words that don’t specify the product by any means (based on the stopwords list)

Methodology and Possible Approaches
Cosine Similarity & TF-IDF Vectorization
Fuzzy
Both methods are discussed in more detail further in the report.
Cosine Similarity with TF-IDF Vectorization
CosSimilarity.py

Why can Cosine Similarity be a good approach for this problem?
Cosine similarity works well for short text comparisons, such as product names. It also handles variations in word order.
Method
The fuzzy approach applies token-set-ratio which tokenizes each product name into sets of words and compares them based on overlap. This technique is robust to word order and extra words, making it ideal for matching variations of product names. An adjustable threshold controls sensitivity of the comparison (threshold 70 resulted in the most cohesive groups).
Initially, I tested pairwise matching which finds a match for each product using the threshold and reports pairs of matching products. However, since multiple similar product names appeared in each dataset, I changed the algorithm to perform cluster-based grouping, which groups all similar products into clusters instead of just pairs.
Results of both methods get saved as Excel files.


Fuzzy
fuzzy.py

Why can fuzzy work?
Fuzzy matching allows for uncertainty in text and measures similarity even when there are variations in wording.
Method
The algorithm applies token-based matching using rapidfuzz. An adjustable threshold controls sensitivity of the comparison (threshold 70 resulted in the most cohesive groups).
Initially, I tested pairwise matching which finds a match for each product using the threshold and reports pairs of matching products. However, since multiple similar product names appeared in each dataset, I changed the algorithm to perform cluster-based grouping, which groups all similar products into clusters instead of just pairs.
Results of both methods get saved as Excel files.
