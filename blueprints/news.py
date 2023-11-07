from flask_login import login_required
from flask import Blueprint, jsonify, request
from config.config import Config
from summarizer.summarizer import (
    generate_summary,
) 
from eventregistry import *
import random


news_bp = Blueprint("news", __name__)

@news_bp.route("/get-news/<string:source>", methods=['GET'])
def fetch_articles_for_outlet(source):
    api_key = Config.NEWS_API_KEY

    # Replace 'YOUR_API_KEY' with your actual API key
    er = EventRegistry(apiKey=api_key, allowUseOfArchive=False)

    # Define the source name
    source_uri = source  # Use the source parameter from the route
    random_page = random.randint(1, 5)

    # Get the page number from the request (use 1 if not provided)
    page = int(request.args.get('page', random_page))

    # Define your query using QueryArticlesIter
    q = QueryArticlesIter(
        sourceUri=source_uri
    )

    # Configure and execute the query to get one article at a time
    q.setRequestedResult(RequestArticlesInfo(page=page, count=1, sortBy="date", sortByAsc=False))
    article = next(q.execQuery(er), None)

    # Check if an article was found
    if article:
        article_info = {
            "title": article["title"],
            "description": article["body"],
            "url": article["url"],
            "date": article["date"],
        }
    else:
        article_info = None

    # Don't close the Event Registry connection here

    return jsonify(article_info)