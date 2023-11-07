# Multi-Document Summarizer As a Service
> Official repository for the [Docker AI/ML Hackathon 2023](https://docker.devpost.com/)
### Powered by 
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

## Table of Contents
- [About the App](#about-the-app)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [License](#license)

## About the App
Multi-document Summarizer as a Service is a cloud-based platform that empowers users to efficiently summarize multiple documents,  leveraging AI, into concise, coherent summaries. 

✅ If you're a busy professional who wants to summarize the news, don't worry; you can use our news model to import and summarize your daily information.

✅ If you're a student with numerous PDFs and documents and don't have time to go through them all, you can use our multi-document summarization model.

✅ If you simply want to save time and avoid unnecessary text, no problem – we've got your back.

**Key Features:**

- **Source Selection:** Choose from a variety of reputable news sources, including The Wall Street Journal, BBC, Europa Press, and more.

- **Random Article Retrieval:** Get a random article from your selected source each time you use the app.

- **Article Summaries:** View concise summaries of news articles, making it easy to stay informed quickly.

- **Save to Documents:** Easily save interesting articles as documents for future reference.

- **Responsive Design:** Access the app seamlessly on various devices, from desktops to smartphones.

"News Aggregator" stands out by providing users with a tailored news experience. Whether you want to catch up on global news, follow industry updates, or stay informed about specific topics, our app has you covered. Say goodbye to information overload and hello to a more streamlined news-reading experience.

We're committed to continually improving and expanding our app's capabilities to enhance your news consumption. Thank you for choosing "News Aggregator."


## Technologies Used
Outline the technologies and tools used in your project. Include programming languages, frameworks, libraries, databases, and any other important tech stack components.

- Python
- Flask
- PostgreSQL
- JavaScript
- Docker
- HTML/CSS

## Features

- **Homepage**: The application includes a simple homepage that introduces users to the text summarization service. It displays a welcome message and provides a link to access the summarization API.

- **Summarization API**: The API accepts a list of documents and generates a summary of the combined text. Users can submit documents via a POST request to the `/summarize` endpoint.

## Project Structure

The current project directory is organized as follows:
```bash
root/
├── run.py # Flask application script for startup
├── app.py # Factory pattern
├── requirements.txt # All needed libs
├── blueprints/
├── models.py # Models used in the app
├── docker-compose.yml # Docker configuration
├── summarizer/ # Summarization module
│ └── summarizer.py # Summarization logic
├── templates/ # HTML templates
│ └── auth/ # Login and Register UI
│ └── main/ # Dashboard and main part of the App
├── tests/
├── static/
├── config/ # Factory pattern settings
```


## Getting Started

To run the application, follow these steps:

1. Ensure you have Flask installed. If not, you can install it using 
```bash	
pip install -r requirements.txt
```

2. Modify the summarization logic in `summarizer_nltk/summarizer.py` to suit your summarization requirements. [Current model used is nltk, more models will be added in the future]

3. Start the Flask application by running the following command in the root directory:

```bash
python run.py
``` 

4. Access the homepage at `http://127.0.0.1:5000/` or `http://localhost:5000/` and use the register to start.


## API Documentation

You can customize the appearance and functionality of the homepage and the summarization API to meet your project's requirements. You can also add more advanced summarization techniques or integrate other NLP libraries as needed. (homepage Frontend currently uses Bootstrap, found in `templates/index.html`)


## License

This project is licensed under the Apache License. [See LICENSE](LICENSE) for more details.
