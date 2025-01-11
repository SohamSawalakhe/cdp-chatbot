# Customer Data Platform (CDP) Documentation Chatbot

This project implements a chatbot that answers user queries related to the documentation of four major Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap. The chatbot extracts information from the official documentation pages of these platforms and provides the most relevant answers based on the user's question.

## Features

- NLP-based question processing using spaCy.
- Search for relevant information in the official documentation using Google Custom Search API.
- Fall back to web scraping using BeautifulSoup if the search API doesn't return satisfactory results.
- Built using Django as the backend framework.

## How it works

1. The user submits a question.
2. The chatbot processes the question using spaCy to extract relevant keywords.
3. The chatbot searches for documentation based on the extracted keywords.
4. If Google Custom Search fails, it falls back to web scraping the documentation pages.
5. The chatbot returns the most relevant answer based on the results.

## Requirements

- Django
- spaCy
- BeautifulSoup
- requests
- Google Custom Search API (for fetching search results)

## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/cdp-chatbot.git
   cd cdp-chatbot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Django server:

   ```bash
   python manage.py runserver
   ```

4. Access the chatbot in your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
