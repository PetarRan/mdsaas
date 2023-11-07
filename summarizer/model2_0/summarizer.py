import nltk
import spacy
from nltk.corpus import stopwords
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Set up NLTK
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Set up SpaCy
nlp = spacy.load("en_core_web_sm")

# Load your input document (txt, pdf, docx) and extract text
# Replace "your_document.txt" with your document path
with open("your_document.txt", "r") as file:
    document_text = file.read()

# NLTK Summarization
# You can choose different NLTK summarization algorithms (e.g., TextRank, LexRank)
# See NLTK documentation for more options.
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.cluster.util import cosine_distance
import numpy as np

def nltk_summarize(document_text, num_sentences=3):
    sentences = sent_tokenize(document_text)
    words = word_tokenize(document_text)
    words = [word.lower() for word in words if word.isalnum()]
    words = [word for word in words if word not in stop_words]

    word_freq = FreqDist(words)
    max_freq = max(word_freq.values())

    for word in word_freq:
        word_freq[word] = word_freq[word] / max_freq

    sentence_scores = []
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = word_freq[word]

    summary_sentences = sorted(
        sentence_scores.items(), key=lambda x: x[1], reverse=True
    )[:num_sentences]
    summary = [sentence for sentence, score in summary_sentences]

    return " ".join(summary)

nltk_summary = nltk_summarize(document_text)

# SpaCy Summarization
# You can customize the summarization method based on your preferences.
def spacy_summarize(document_text, num_sentences=3):
    doc = nlp(document_text)
    sentences = [sent.text for sent in doc.sents]
    return " ".join(sentences[:num_sentences])

spacy_summary = spacy_summarize(document_text)

# Sumy Summarization
def sumy_summarize(document_text, num_sentences=3):
    parser = PlaintextParser.from_string(document_text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join([str(sentence) for sentence in summary])

sumy_summary = sumy_summarize(document_text)

# Combine Summaries
final_summary = f"NLTK Summary:\n{nltk_summary}\n\nSpaCy Summary:\n{spacy_summary}\n\nSumy Summary:\n{sumy_summary}"

# Save or display the final summary
with open("final_summary.txt", "w") as output_file:
    output_file.write(final_summary)
