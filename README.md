# Multi-Document Summarizer As a Service
> Official repository for the [Docker AI/ML Hackathon 2023](https://docker.devpost.com/)
### Powered by 
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

## Table of Contents
- [About the App](#about-the-app)
- [Technologies Used](#technologies-used)
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

- **Article Summaries:** View concise summaries of news articles, making it easy to stay informed quickly.

- **Save to Documents:** Easily save interesting articles as documents for future reference.

- **Responsive Design:** Access the app seamlessly on various devices, from desktops to smartphones.

## Technologies Used
Outline the technologies and tools used in your project. Include programming languages, frameworks, libraries, databases, and any other important tech stack components.

- Python
- Flask
- PostgreSQL
- JavaScript
- Docker
- [News API](https://newsapi.ai/)
- HTML/CSS

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


# API Documentation

## Table of Contents

1. [Authentication](#authentication)
    - [Login](#login)
    - [Logout](#logout)
    - [Register](#register)

2. [Documents](#documents)
    - [Get All Documents](#get-all-documents)
    - [Delete Document](#delete-document)
    - [Get Document Content](#get-document-content)
    - [Upload Document](#upload-document)
    - [Upload Document from Link](#upload-document-link)
    - [Upload Document from News](#upload-document-news)

3. [News](#news)
    - [Fetch Articles for Outlet](#fetch-articles-for-outlet)

4. [Summarizer](#summarizer)
    - [Get All Summaries](#get-all-summaries)
    - [Get Summary Content](#get-summary-content)
    - [Delete Summary](#delete-summary)
    - [Summarize Documents](#summarize-documents)

## Authentication <a name="authentication"></a>

### Login <a name="login"></a>

- **URL:** `/login`
- **Method:** POST
- **Description:** Log in with your username and password.
- **Request:**
  - `username` (string): Your username.
  - `password` (string): Your password.
- **Response:**
  - If successful, it redirects to `/dashboard`.
  - If unsuccessful, returns an error message with status 401.

### Logout <a name="logout"></a>

- **URL:** `/logout`
- **Method:** GET
- **Description:** Log out the user.
- **Response:**
  - Clears the user session and redirects to `/login`.

### Register <a name="register"></a>

- **URL:** `/register`
- **Method:** POST
- **Description:** Register a new user.
- **Request:**
  - `username` (string): Desired username.
  - `password` (string): Password.
  - `email` (string): Email address.
- **Response:**
  - If successful, redirects to `/login?success=true`.
  - If the username is already taken, returns an error message with status 400.

## Documents <a name="documents"></a>

### Get All Documents <a name="get-all-documents"></a>

- **URL:** `/get-all-documents`
- **Method:** GET
- **Authentication:** Login required.
- **Description:** Get all documents for the current user.
- **Response:**
  - JSON array of documents with fields:
    - `name` (string): Document title.
    - `dateUploaded` (string): Date of upload.
    - `id` (int): Document ID.
    - `content` (string): Document content.
    - `user` (string): Username of the owner.

### Delete Document <a name="delete-document"></a>

- **URL:** `/delete-document/<int:document_id>`
- **Method:** DELETE
- **Authentication:** Login required.
- **Description:** Delete a document by its ID for the current user.
- **Response:**
  - If successful, returns a success message.
  - If the document does not belong to the user, returns an error message with status 403.
  - If the document is not found, returns an error message with status 404.

### Get Document Content <a name="get-document-content"></a>

- **URL:** `/get-document-content/<int:document_id>`
- **Method:** GET
- **Authentication:** Login required.
- **Description:** Get the content of a document by its ID for the current user.
- **Response:**
  - If successful and the document belongs to the user, returns the document content.
  - If unauthorized, returns an error message with status 403.
  - If the document is not found, returns an error message with status 404.

### Upload Document <a name="upload-document"></a>

- **URL:** `/upload-document`
- **Method:** POST
- **Authentication:** Login required.
- **Description:** Upload a document for the current user.
- **Request:**
  - Multiple files with names like `content0`, `content1`, etc.
  - Optional title for each document: `title0`, `title1`, etc.
- **Response:**
  - If successful, returns a JSON object with document IDs and a success message.
  - If no valid documents are uploaded, returns an error message with status 400.
  - If no content is provided, returns an error message with status 400.

### Upload Document from Link <a name="upload-document-link"></a>

- **URL:** `/upload-document-link`
- **Method:** POST
- **Authentication:** Login required.
- **Description:** Upload a document from a link for the current user.
- **Request:**
  - `link` (string): URL of the document.
  - Optional `title` (string): Title of the document (default is "Untitled").
- **Response:**
  - If successful, returns a JSON object with the document ID and a success message.
  - If failed to fetch the document content, returns an error message with status 400.

### Upload Document from News <a name="upload-document-news"></a>

- **URL:** `/upload-document-news`
- **Method:** POST
- **Authentication:** Login required.
- **Description:** Upload a document from news for the current user.
- **Request:**
  - `title` (string): Title of the news article.
  - `content` (string): Content of the news article.
- **Response:**
  - If successful, returns a JSON object with the document ID and a success message.
  - If failed to fetch the document content, returns an error message with status 400.

## News <a name="news"></a>

### Fetch Articles for Outlet <a name="fetch-articles-for-outlet"></a>

- **URL:** `/get-news/<string:source>`
- **Method:** GET
- **Description:** Fetch articles for a news outlet.
- **Request:**
  - `source` (string): News outlet source.
- **Response:**
  - If successful, returns information about an article:
    - `title` (string): Article title.
    - `description` (string): Article content.
    - `url` (string): Article URL.
    - `date` (string): Article publication date.

## Summarizer <a name="summarizer"></a>

### Get All Summaries <a name="get-all-summaries"></a>

- **URL:** `/get-all-summaries`
- **Method:** GET
- **Authentication:** Login required.
- **Description:** Get all summaries for the current user.
- **Response:**
  - JSON array of summaries with fields:
    - `summary_id` (int): Summary ID.
    - `generated_summary` (string): Generated summary.
    - `method` (string): Summarization method.

### Get Summary Content <a name="get-summary-content"></a>

- **URL:** `/get-summary-content/<int:summary_id>`
- **Method:** GET
- **Authentication:** Login required.
- **Description:** Get the content of a summary by its ID for the current user.
- **Response:**
  - If successful and the summary belongs to the user, returns the summary content.
  - If unauthorized, returns an error message with status 403.
  - If the summary is not found, returns an error message with status 404.

### Delete Summary <a name="delete-summary"></a>

- **URL:** `/delete-summary/<int:summary_id>`
- **Method:** DELETE
- **Authentication:** Login required.
- **Description:** Delete a summary by its ID for the current user.
- **Response:**
  - If successful, returns a success message.
  - If the summary does not belong to the user, returns an error message with status 403.
  - If the summary is not found, returns an error message with status 404.

### Summarize Documents <a name="summarize-documents"></a>

- **URL:** `/summarize`
- **Method:** POST
- **Authentication:** Login required.
- **Description:** Generate a summary for a list of documents.
- **Request:**
  - `documents` (list of strings): List of document content for summarization.
  - `summarization_method` (string): Chosen summarization method.
- **Response:**
  - If successful, returns a success message.


## License

This project is licensed under the Apache License. [See LICENSE](LICENSE) for more details.
