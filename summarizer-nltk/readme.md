# Multi-Document Text Summarization as a Service

## Prerequisites

Before running the code, ensure that you have the following prerequisites installed:

- Python 3.x
- `pip` (Python package manager)

## Setup

1. Clone the repository or download the code.

2. Open your terminal or command prompt and navigate to the project directory.

3. Install the required Python packages by running the following command:

```bash
pip install nltk
```

4. Navigate to the `summarizer-nltk` directory.

```bash
cd summarizer-nltk
```

5. Run the summarization script by executing the following command:

```bash
python summarizer.py
```

## Usage

Replace `'test-text-to-be-summarized.txt'` in the script with the path to the text document you want to summarize. For example:

```python
input_file = 'your_document.txt'
```

## Example

```bash
python summarizer.py
```

## Output

The script will print the summary to the console.
We might want to keep it this way so we can use it as a service (API) later on. Possiblity is also to print it out in a .txt filed but that's not necessary.

Example output for the test-text-to-be-summarized.txt file:

>Summary:
>Machine learning, a subset of AI, focuses on the development of algorithms that enable machines to learn and make predictions from data.
>Furthermore, AI has made strides in decision-making, allowing machines to make informed choices based on data analysis.
>Computer scientists and mathematicians developed algorithms and models for problem-solving, leading to the birth of modern AI.
>Reinforcement learning, for example, focuses on developing agents that learn to make decisions through trial and error, leading to advancements in areas like robotics and autonomous control systems.
>AI has the potential to address some of the world's most significant challenges, from climate change and healthcare disparities to poverty and education access.



### Additional Notes

- This code provides a basic extractive text summarization model using **NLTK**. For more advanced summarization techniques, consider exploring other NLP libraries and models(maybe SpaCy? I used that one, perhaps its better, anyhoo NLTK, Gensim, or spaCy).

- The script can be further integrated into a web-based service for multi-document text summarization using Docker, WHICH is the goal.

- Please when trying out replace `'your_input.txt'` with the actual path to your input text document in the script as needed. 

> This Markdown file provides instructions on setting up the environment, running the script, and additional notes for customization and integration into our project.
