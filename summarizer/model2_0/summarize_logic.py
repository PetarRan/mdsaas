import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
## This is not found in requirements.txt make sure to pip install networkx
import networkx as nx

nltk.download('punkt')
nltk.download('stopwords')

def sentence_similarity(sent1, sent2, stopwords):
    # Function to compute the similarity between two sentences using cosine similarity

    # Tokenize and remove stopwords
    sent1 = [word for word in sent1 if word not in stopwords]
    sent2 = [word for word in sent2 if word not in stopwords]

    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # Build vectors for each sentence
    for word in sent1:
        vector1[all_words.index(word)] += 1

    for word in sent2:
        vector2[all_words.index(word)] += 1

    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stopwords):
    # Create a matrix of sentence similarities
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:
                continue
            similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stopwords)

    return similarity_matrix

def generate_summary(document, num_sentences):
    # Summarization logic: Extract the top 'num_sentences' important sentences using TextRank

    # Tokenize the document into sentences
    sentences = nltk.sent_tokenize(document)

    # Create a list of stopwords
    stop_words = set(stopwords.words('english'))

    # Generate the sentence similarity matrix
    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)

    # Apply PageRank algorithm to get sentence rankings
    sentence_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_graph)

    # Sort the sentences by score in descending order
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    # Extract the top 'num_sentences' sentences as the summary
    summary = [ranked_sentences[i][1] for i in range(num_sentences)]

    return ' '.join(summary)
