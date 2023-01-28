from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown2 import Markdown
import random

from . import util

""" 
    if request.GET.get('q'):
        return search(request, request.GET.get('q'))
        
    Checks if there is a search query present
"""
    
def index(request):
    if request.GET.get('q'):
        return search(request, request.GET.get('q')) 
    # Default page, i.e., index.html, is displayed if search query is not present
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    

def search(request, title):
    # Empty list that will be used for storing entry title containing title substring
    entries = []
    
    """ Check if there are multiple occurrences of the substring in entry titles """
    for match in util.list_entries():
        # Case insensitive
        if match.upper().find(title.upper()) != -1:
            entries.append(match)
    
    match = True
    
    # No match found for the search query
    if not len(entries):
        entries.append(f"No matches found for \"{title}\".")
        match = False
        
    return render(request, "encyclopedia/list-of-entries.html", {
        "title": title,
        "entries": entries,
        "match": match
        })
    

def entry(request, title):
    if request.GET.get('q'):
        return search(request, request.GET.get('q'))
    # Check if there is an entry with the given title
    # If so, render entry page
    elif request.method == 'GET' and title in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": Markdown().convert(util.get_entry(title))
        })
    # Otherwise, display error page
    else:
        return HttpResponseRedirect("/error.html")
    

# TODO - Create New Page
def newpage(request):
    if request.GET.get('q'):
        return search(request, request.GET.get('q')) 
    # Render "Create New Page" page if the method is GET and there is no search query
    elif request.method == "GET":
        return render(request, "encyclopedia/new-page.html")
    
    
    title = request.POST.get('title')
    # Check if there's an entry by that title 
    if title in util.list_entries():
        return HttpResponseRedirect("/error.html")
    
    content = request.POST.get('content')
    saved = request.POST.get('save')
    
    if content and saved:
        util.save_entry(title, content)
    
    # PRG => POST redirect GET, lest to submit the same form multiple times
    return HttpResponseRedirect(f"/wiki/{title}")

def editpage(request):
    title = request.GET.get('title')
    
    if request.GET.get('q'):
        return search(request, request.GET.get('q'))
    elif request.method == "GET":
        return render(request, "encyclopedia/edit-page.html", {
            "title": title,
            "content": util.get_entry(title)
        })
    
    title = request.POST.get('title')
    content = request.POST.get('content')
    saved = request.POST.get('save')
    
    if content and saved:
        util.save_entry(title, content)
        return HttpResponseRedirect(f"/wiki/{title}")
    

def error(request):
    if request.GET.get('q'):
        return search(request, request.GET.get('q'))
    
    return render(request, "encyclopedia/error.html")

def randompage(request):
    return HttpResponseRedirect(f"/wiki/{random.choice(util.list_entries())}")
