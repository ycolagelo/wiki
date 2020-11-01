from random import choice
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django import forms
import markdown2
from .error_codes import TITLE_ALREADY_EXISTS, ERROR_MESSAGES, FORM_IS_INVALID, NOT_FOUND


from . import util


def index(request):
    """ Lists all the entries"""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    """ displays details of the tile"""
    my_entry = util.get_entry(title)
    if my_entry:
        formatted = markdown2.markdown(my_entry)
        return render(request, "encyclopedia/entry.html", {
            "entry": formatted,
            "title": title
        })

    return redirect("error", code=NOT_FOUND)


def search(request):
    """ The search view """
    if 'q' in request.GET:
        query = request.GET['q'].strip()
        my_entry = util.get_entry(query)
        possible_entries = util.search_entries(query)
        if my_entry:
            # redirect to entry
            return redirect("entry", title=query)
        if possible_entries:
            # show search results page
            return render(request, "encyclopedia/search.html", {"entries": possible_entries})
    else:
        return HttpResponseBadRequest("q is required")


class NewEntryForm(forms.Form):
    """adding a class for my form entry"""
    title = forms.CharField(label="the title")
    detail = forms.CharField(label="the details")


class EditEntryForm(forms.Form):
    """form to edit an entry"""
    detail = forms.CharField(label="the details")


def add(request):
    """Handles the form by checking if the form is valid,
    if it already exists and saves the form if it passes validation"""
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            new_entry = form.cleaned_data["detail"]
            current_list = util.list_entries()
            if title in current_list:
                return redirect("error", code=TITLE_ALREADY_EXISTS)
            else:
                util.save_entry(title, new_entry)
                return redirect("entry", title=title)
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm()
    })


def edit(request, title):
    """Handles the editing of the existing page"""

    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            new_entry = form.cleaned_data["detail"]
            util.save_entry(title, new_entry)
            return redirect("entry", title=title)
        else:
            # form is invalid, error message
            return redirect("error", code=FORM_IS_INVALID)
    else:
        # GET
        # title = request.Get["title"]
        my_entry = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "entry": my_entry
        })


def random(request):
    """generates a random page for the user"""
    entries = util.list_entries()
    title = choice(entries)
    return redirect("entry", title=title)


def error(request, code):
    """generates an error page using the error_codes"""
    error_message = ERROR_MESSAGES[code]

    return render(request, "encyclopedia/error.html", {
        "error": error_message
    })
