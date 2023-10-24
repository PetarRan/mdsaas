import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance

def read_text_from_file(file_path):
   with open(file_path, 'r') as file:
       text = file.read()
   return text

def sentence_similarity(sent1, sent2, stopwords=None):
   if stopwords is None:
       stopwords = []
   sent1 = [w.lower() for w in sent1]
   sent2 = [w.lower() for w in sent2]

   all_words = list(set(sent1 + sent2))

   vector1 = [0] * len(all_words)
   vector2 = [0] * len(all_words)

   for w in sent1:
       if w in stopwords:
           continue
       vector1[all_words.index(w)] += 1

   for w in sent2:
       if w in stopwords:
           continue
       vector2[all_words.index(w)] += 1

   return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
   similarity_matrix = [[0 for _ in range(len(sentences))] for _ in range(len(sentences))]

   for i in range(len(sentences)):
       for j in range(len(sentences)):
           if i != j:
               similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stop_words)

   return similarity_matrix

def generate_summary(file_path, top_n=5):
   nltk.download('punkt')
   nltk.download('stopwords')

   stop_words = set(stopwords.words('english'))
   text = read_text_from_file(file_path)
   sentences = sent_tokenize(text)

   sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)

   # Calculate sentence scores based on similarity matrix (without NetworkX)
   scores = [sum(sentence_similarity_matrix[i]) for i in range(len(sentences))]

   # Rank sentences by score and select the top N sentences
   ranked_sentences = [sentences[i] for i in sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)][:top_n]

   summary = "\n".join(ranked_sentences)
   return summary

if __name__ == "__main__":
   input_file = 'test-text-to-be-summarized.txt'  # Replace with your input file path
   summary = generate_summary(input_file)
   print("Summary:\n", summary)
