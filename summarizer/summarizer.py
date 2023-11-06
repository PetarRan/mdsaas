import nltk
import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.cluster.util import cosine_distance

nltk.download("punkt")
nlp = spacy.load("en_core_web_sm")

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

def nltk_summarize(text, top_n=5):
   nltk.download('punkt')
   nltk.download('stopwords')

   stop_words = set(stopwords.words('english'))
   sentences = sent_tokenize(text)

   sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)

   # Calculate sentence scores based on similarity matrix (without NetworkX)
   scores = [sum(sentence_similarity_matrix[i]) for i in range(len(sentences))]

   # Rank sentences by score and select the top N sentences
   ranked_sentences = [sentences[i] for i in sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)][:top_n]

   summary = "\n".join(ranked_sentences)
   return summary

# SpaCy Summarization
def spacy_summarize(text):
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    summary_sentences = sentences[:3]  # Return the first 3 sentences as a summary
    return " ".join(summary_sentences)

# Sumy Summarization
def sumy_summarize(text):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)  # Summarize into 3 sentences
    return " ".join([str(sentence) for sentence in summary])

# Main summarization function
def generate_summary(texts, summarization_method):
    if summarization_method == "nltk":
        return nltk_summarize(" ".join(texts))
    elif summarization_method == "spacy":
        return spacy_summarize(" ".join(texts))
    elif summarization_method == "sumy":
        return sumy_summarize(" ".join(texts))
    else:
        return "Invalid summarization method."

if __name__ == "__main__":
    input_texts = ["As AI continues to advance, the challenges and ethical concerns surrounding it have also grown. Issues related to data privacy have become paramount. AI systems often require large datasets for training, raising concerns about the security and privacy of user data. Bias in AI algorithms has become a significant concern, as AI systems can perpetuate or even exacerbate existing biases in society. Additionally, the impact of AI on employment is a topic of ongoing debate. While AI can automate certain tasks, it also has the potential to create new job opportunities and enhance productivity. AI is now a multi-faceted field with numerous sub-disciplines. Reinforcement learning, for example, focuses on developing agents that learn to make decisions through trial and error, leading to advancements in areas like robotics and autonomous control systems. Neural networks, inspired by the human brain, have become a cornerstone of deep learning, enabling breakthroughs in image and speech recognition. Robotics is an interdisciplinary field that combines AI, engineering, and mechanics to create intelligent machines capable of performing physical tasks. AI has a vast potential for transforming industries and improving the quality of life. In healthcare, AI can aid in early disease detection, drug discovery, and personalized treatment plans. In education, AI can enhance the learning experience through adaptive tutoring and personalized curriculum recommendations. In agriculture, AI-powered drones and sensors can optimize crop management. The applications of AI are diverse and far-reaching. However, the responsible development and ethical use of AI are paramount to ensure a positive impact on society. Ethical AI development includes transparency in algorithms, fairness in decision-making, and adherence to data privacy regulations. It is crucial to ensure that AI technologies are accessible, beneficial, and accountable to all members of society. The future of AI holds great promise. It will likely continue to shape the way we live, work, and interact with technology. AI has the potential to address some of the world's most significant challenges, from climate change and healthcare disparities to poverty and education access. The development of AI will be driven not only by technological advancements but also by a commitment to addressing the social and ethical challenges that it presents. As AI continues to evolve, it is our responsibility to guide its development in a way that benefits humanity as a whole.", 
                   "Since then, AI has made remarkable progress. It has evolved from rule-based expert systems to machine learning and deep learning approaches. Machine learning, a subset of AI, focuses on the development of algorithms that enable machines to learn and make predictions from data. Deep learning, in particular, has revolutionized AI by enabling the training of neural networks, leading to significant breakthroughs in tasks like image recognition and natural language understanding. AI-powered systems are now capable of natural language processing, allowing machines to understand and generate human language. Computer vision enables machines to interpret and process visual information, making applications like facial recognition and object detection possible. Speech recognition technology has advanced to the point where virtual assistants like Siri and Alexa can understand and respond to spoken commands. Furthermore, AI has made strides in decision-making, allowing machines to make informed choices based on data analysis. This progress has led to the integration of AI into various applications, from self-driving cars that rely on AI algorithms to navigate and make driving decisions to healthcare diagnosis where AI can assist in the interpretation of medical images and suggest treatment options. AI's impact is felt across industries, from finance and retail to education and entertainment.", 
                   "The history of artificial intelligence (AI) dates back to ancient times when myths and stories featured automatons and intelligent mechanical beings. These early tales sparked human imagination, giving rise to the idea of creating machines that can mimic human cognitive functions. The dream of machines emulating human thought processes has been a part of human culture for centuries. Fast forward to the 20th century, and AI began to take shape as a formal discipline. Computer scientists and mathematicians developed algorithms and models for problem-solving, leading to the birth of modern AI. The famous Dartmouth Workshop in 1956, organized by John McCarthy and Marvin Minsky, is often considered the birth of AI as a field. This event marked the first time that AI was recognized as a distinct area of study."]
    summarization_method = "nltk"  # Change this to "spacy" or "sumy" as needed
    summary = generate_summary(input_texts, summarization_method)
    print("Summary:\n", summary)
