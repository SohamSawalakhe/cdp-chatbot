from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import spacy
import requests
from bs4 import BeautifulSoup

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Google Custom Search API settings
API_KEY = 'AIzaSyB8JDD1g_mwnFhoIPkxyGvaw10VXJHKpDM'  # Replace with your Google API key
CSE_ID = '8670e3265ee3b4c0c'  # Replace with your Custom Search Engine ID

# Documentation URLs for the four CDPs
DOCUMENTATION_URLS = {
    "segment": "https://segment.com/docs/?ref=nav",
    "mparticle": "https://docs.mparticle.com/",
    "lytics": "https://docs.lytics.com/",
    "zeotap": "https://docs.zeotap.com/home/en-us/",
}

def process_question(question):
    """
    Process the user's question to extract key tokens using spaCy.
    """
    doc = nlp(question)
    return [token.text.lower() for token in doc]

def search_documentation_with_google_api(cdp, question):
    """
    Use Google Custom Search API to search for relevant information in the documentation.
    If the GCP search fails, fall back to BeautifulSoup scraping.
    """
    url = DOCUMENTATION_URLS.get(cdp)
    if not url:
        return "Documentation URL not found for this platform."

    # Prepare the query with the user's question and documentation URL
    query = f"{question} site:{url}"

    # Google Custom Search API URL
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}"

    try:
        # Make the request to Google Custom Search API
        response = requests.get(search_url)
        response.raise_for_status()

        search_results = response.json()
        items = search_results.get("items", [])

        if items:
            # Return the top result's snippet and title
            top_result = items[0]
            return f"Here's what I found: {top_result['snippet']} (Source: {top_result['title']})"
        else:
            return "No relevant information found in the documentation. Attempting BeautifulSoup fallback."

    except Exception as e:
        return f"Error while searching: {e}, trying BeautifulSoup fallback."

def search_documentation_with_beautifulsoup(cdp, question):
    """
    Scrape the documentation page using BeautifulSoup if GCP fails.
    """
    url = DOCUMENTATION_URLS.get(cdp)
    if not url:
        return "Documentation URL not found for this platform."

    try:
        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.get_text().lower()

        # Search for the question keywords in the page content
        question_tokens = set(process_question(question))
        lines = content.split("\n")
        relevant_lines = [
            line.strip() for line in lines if any(token in line for token in question_tokens)
        ]

        if relevant_lines:
            return " ".join(relevant_lines[:5])
        else:
            return "No relevant information found in the documentation using BeautifulSoup."

    except Exception as e:
        return f"Error while scraping: {e}"

def get_cdp_from_question(tokens):
    """
    Determine which CDP the question is about based on keywords in the question.
    """
    if any(token in ["segment", "source", "tracking"] for token in tokens):
        return "segment"
    if any(token in ["mparticle", "user", "profile"] for token in tokens):
        return "mparticle"
    if any(token in ["lytics", "audience", "segment"] for token in tokens):
        return "lytics"
    if any(token in ["zeotap", "integration", "data"] for token in tokens):
        return "zeotap"
    return None

@csrf_exempt
def ask_question(request):
    if request.method == "POST":
        # Get the user's question
        question = request.POST.get("question", "").strip()
        if not question:
            return JsonResponse({"answer": "Please ask a valid question."})

        # Process the question to extract tokens
        tokens = process_question(question)

        # Identify the target CDP
        cdp = get_cdp_from_question(tokens)
        if not cdp:
            return JsonResponse(
                {
                    "answer": "I couldn't identify which platform your question is about. "
                    "Please specify Segment, mParticle, Lytics, or Zeotap."
                }
            )

        # First try Google Custom Search
        answer = search_documentation_with_google_api(cdp, question)

        # If GCP didn't return satisfactory results, fallback to BeautifulSoup scraping
        if "No relevant information found" in answer:
            answer = search_documentation_with_beautifulsoup(cdp, question)

        return JsonResponse({"answer": answer})

    return JsonResponse({"error": "Invalid request"}, status=400)

def index(request):
    return render(request, "chatbot/index.html")
