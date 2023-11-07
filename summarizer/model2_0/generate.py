from summarize_logic import generate_summary

# Load a sample document (replace with your actual document)
document = """
This is a sample document. It contains multiple sentences. You can use this document for testing and fine-tuning your summarization method.
"""

# Define the number of sentences you want in the summary
num_sentences = 3

# Generate the summary using the function
summary = generate_summary(document, num_sentences)

# Print the generated summary
print("Generated Summary:")
print(summary)
