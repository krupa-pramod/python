from urllib.request import urlopen
from urllib.parse import urlencode
from json import loads, load, dump, dumps


def get_artworks(search_term, max_results):
    BASE_API_URL = "https://api.harvardartmuseums.org"
    endpoint = "/image"
    API_KEY = "f83b19c6-9ac2-4e90-a2fa-f49e17f4f257"
    query_params = {
        "apikey": API_KEY,
        "q": search_term,
        "size": max_results,
    }
    encoded_query_params = urlencode(query_params)
    request_url = f"{BASE_API_URL}{endpoint}?{encoded_query_params}"

    with urlopen(request_url) as response:
        response_data = loads(response.read())

    return response_data["records"]


def get_articles(search_term, max_results):
    BASE_API_URL = "https://newsapi.org/v2"
    endpoint = "/everything"
    API_KEY = "91cf9a43020d4980abf16073fc1ff0d3"
    query_params = {
        "apikey": API_KEY,
        "q": search_term,
        "pageSize": max_results,
    }
    encoded_query_params = urlencode(query_params)
    request_url = f"{BASE_API_URL}{endpoint}?{encoded_query_params}"

    with urlopen(request_url) as response:
        response_data = loads(response.read())

    return response_data["articles"]


def get_books(search_term, max_results):
    BASE_API_URL = "https://gutendex.com"
    endpoint = "/books"
    query_params = {
        "search": search_term,
    }
    encoded_query_params = urlencode(query_params)
    request_url = f"{BASE_API_URL}{endpoint}?{encoded_query_params}"

    with urlopen(request_url) as response:
        books_json = loads(response.read())

    return books_json["results"][:max_results]


def display_articles(articles):
    print("\n************ Article results ************\n")
    for article in articles:
        print(f"\nTitle: {article['title']}")
        print(f"Author: {article['author']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")
    print("\n**********************************************\n")


def display_books(books):
    print("\n************ Book results ************\n")
    for book in books:
        print(f"\nTitle: {book['title']}")
        print(f"Author(s): {book['authors']}")
        print(f"Subjects: {book['subjects']}")
    print("\n**********************************************\n")


def display_artworks(artworks):
    print("\n********** Artwork results **********\n")
    for artwork in artworks:
        print(f"\nDescription: {artwork['description']}")
        print(f"URL: {artwork['baseimageurl']}")
    print("\n*********************************************\n")


def display_welcome_banner():
    welcome_banner = """
            Welcome to your personal Search Engine!

        This app lets you provide a search term and then
        returns book/art/news results based on that
        search term.

        You can save selections that you enjoy to browse later!
    """
    print(welcome_banner)


def save_search_results(search_term, artworks, books, articles, username):
    search_results = load_search_results()

    if search_results.get(username) is None:
        search_results[username] = {}

    search_results[username][search_term] = {
        "artworks": artworks,
        "books": books,
        "articles": articles,
    }

    with open("search-results.json", mode="wt") as json_file:
        dump(search_results, json_file, indent="4")


def load_search_results():
    with open("search-results.json", mode="rt") as json_file:
        search_results = load(json_file)

    return search_results


def view_search_results():
    search_results = load_search_results()
    print(dumps(search_results, indent="4"))


options = """
    1.) Search 2.) Save Search Results 3.) View Saved Search Results 4.) Exit
"""

SEARCH = 1
SAVE = 2
VIEW = 3
EXIT = 4

search_term = ""
artworks = []
books = []
articles = []
username = input("username: ")

display_welcome_banner()

while True:
    user_choice = int(input(options))

    if user_choice == SEARCH:
        search_term = input("Enter your search term: ")
        max_results = int(input("How many results do you want? "))

        artworks = get_artworks(search_term, max_results)
        books = get_books(search_term, max_results)
        articles = get_articles(search_term, max_results)

        display_artworks(artworks)
        display_books(books)
        display_articles(articles)
    elif user_choice == SAVE:
        save_search_results(search_term, artworks, books, articles, username)
    elif user_choice == VIEW:
        view_search_results()
    elif user_choice == EXIT:
        break
