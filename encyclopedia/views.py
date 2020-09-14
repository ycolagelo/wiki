from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


from . import util




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })

def details(request):
    # title = title
    print("todo")




