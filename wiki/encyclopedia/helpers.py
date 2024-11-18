from . import util
from random import choice


def search(keyword):
    """
    Return all entries whose titles match partiay
    or totally with the search keywords
    """
    all_articles = util.list_entries()
    result = []
    for entry in all_articles:
        if keyword.lower() in entry.lower():
            result.append(entry)
    return result


def random_article():
    "Return a random article from all saved articles"
    all_articles = util.list_entries()
    random_element = choice(all_articles)
    return random_element
