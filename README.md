# Multi-Document Summarizer As a Service
> Official repository for the Docker AI/ML Hackathon 2023

## Introduction

This is a Flask-based web service for text summarization. The API endpoint for generating text summaries based on the provided documents is the central piece of the SaaS.

This repository contains the code for the Docker AI/ML Hackathon 2023. The goal of this hackathon is to create a Docker image that can be used to train a machine learning model. The model should be able to do a set of features. 

## Features

- **Homepage**: The application includes a simple homepage that introduces users to the text summarization service. It displays a welcome message and provides a link to access the summarization API.

- **Summarization API**: The API accepts a list of documents and generates a summary of the combined text. Users can submit documents via a POST request to the `/summarize` endpoint.

## Project Structure

The current project directory is organized as follows:
```bash
root/
├── app.py # Flask application script
├── summarizer_nltk/ # Summarization module
│ └── summarizer.py # Summarization logic
├── templates/ # HTML templates
│ └── index.html # Homepage template
├── ...
```

### Powered by 
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)


## Getting Started

To run the application, follow these steps:

1. Ensure you have Flask installed. If not, you can install it using 
```bash	
pip install flask
```

2. Modify the summarization logic in `summarizer_nltk/summarizer.py` to suit your summarization requirements. [Current model used is nltk, more models will be added in the future]

3. Start the Flask application by running the following command in the root directory:

```bash
python app.py
``` 

4. Access the homepage at `http://localhost:5000/` and use the `/summarize` endpoint to generate text summaries.

## Usage

- **Homepage**: Visit `http://localhost:5000/` to see the homepage.

- **Summarization API**: Send a POST request with a JSON payload containing a list of documents to `http://localhost:5000/summarize`.

Sample request:

```json
{
    "documents": ["Document 1 text", "Document 2 text"]
}
```

## Customization

You can customize the appearance and functionality of the homepage and the summarization API to meet your project's requirements. You can also add more advanced summarization techniques or integrate other NLP libraries as needed. (homepage Frontend currently uses Bootstrap, found in `templates/index.html`)

## Acknowledgments

This Flask application is a simple example of a text summarization service. We shall further enhance it with additional features, user authentication, and more advanced summarization models.

## License

This project is licensed under the Apache License. [See LICENSE](LICENSE) for more details.
