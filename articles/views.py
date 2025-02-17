from django.shortcuts import render
import requests
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

# http://127.0.0.1:8000/api/wikipedia?title=Python_(programming_language)
# http://127.0.0.1:8000/api/wikipedia?title=C_(programming_language)


@api_view(['GET'])
def wikipedia_intro(request):
    # extract params from request
    # if title is not in the URL it defaults to python
    title = request.GET.get('title', 'Python_(programming_language)')
    
    #setup and check the cache
    cache_key = f"wiki_intro_{title}"
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    # call to wikipedias API params
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'prop': 'extracts',
        'images' : 'images',
        'exintro': True,
        'titles': title,
        'format': 'json'
    }

    # http get request
    resp = requests.get(url, params=params)
    data = resp.json()
    pages = data.get('query', {}).get('pages', {})
    intro_text = ""
    for page_id, page in pages.items():
        intro_text = page.get('extract', '')
        break  # Stop after processing the first page

    # build result cache it and return the response
    result = {'title': title, 'intro': intro_text}
    cache.set(cache_key, result, timeout=3600)
    return Response(result)

# http://127.0.0.1:8000/api/wiki?title=C_(programming_language)
@api_view(['GET'])
def new_title(request):
    title = request.GET.get('title')
    print(title)

    # call to wikipedias API params
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'prop': 'extracts',
        'exintro': True,
        'titles': title,
        'format': 'json'
    }

    resp = requests.get(url, params=params)
    data = resp.json()
    print(type(data))
    

    result = {'title': title}
    
    return Response(result)