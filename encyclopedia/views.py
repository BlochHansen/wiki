from tkinter import DOTBOX
from tokenize import Name
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# from django import forms

from encyclopedia import forms
from .forms import entryForm
from . import util
import re, random


def index(request):
    var = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    if name not in util.list_entries():
        return render(request, "encyclopedia/error.html", {"fejl": "This entry don't exists."})
    else:
        text = util.get_entry(name)
        text = re.sub(r'\r\n', '\n', text)
        # Her ændres # til <h >
        for j in range(6, 0, -1):
            pattern = r'#{' + str(j) + '} (.+)\n'
            replacement = '<h' + str(j) + r'>\1</h' + str(j) + '>'
            text = re.sub(pattern, replacement, text)


        # her ændres ** til <b>
        pattern     = r'\*\*(.+?)\*\*'
        replacement = r'<b>\1</b>'
        text = re.sub(pattern, replacement, text)

        # Her ændres * til <li> </li>
        pattern     = r'\* (.+)\n'
        replacement = r'<li>\1</li>'
        text = re.sub(pattern, replacement, text)
        # så skal der <ul> på
        pattern     = r'(<li>.+)\n'
        replacement = r'<ul>\1</ul>'
        text = re.sub(pattern, replacement, text)


        # Her ændres   til <link>
        pattern     = r'\[(.+?)\]\((.+?)\)'
        replacement = r'<a href="\2">\1</a>'
        text = re.sub(pattern, replacement, text)
    
        # her ændres   til <p>
        pattern     = r'\n(.+)\n\n'
        replacement = r'<p>\1</p>'
        text = re.sub(pattern, replacement, text)

        return render(request, "encyclopedia/entry.html", {
            "text": text,
            "name": name
        })



def query(request):
    if request.method == 'POST':
        var = request.POST["q"]
        entries = []
        for item in util.list_entries():
            if var.lower() == item.lower():
                return HttpResponseRedirect(reverse('entry', args=(var,)))
            else:
                if var.lower() in item.lower():
                    entries.append(item)   
        
        if len(entries) > 0:
            return render(request, "encyclopedia/query.html", {
                "entries": entries
            })
    else:
        return HttpResponse(f"Not Post!")
        

def add(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = entryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            text    = form.cleaned_data["text"]
            title   = form.cleaned_data["title"]
            text = re.sub(r'\r\n', '\n', text)
            # Hvis title allerede eksisterer så error
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {"fejl": "This entry allready exists."})
            else:
                # save file
                util.save_entry(title, text)
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('entry', args=(title,)))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = entryForm()
    return render(request, "encyclopedia/add_entry.html", { 'form': form })

def edit(request, name):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = entryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            text = form.cleaned_data["text"]
            text = re.sub(r'\r\n', '\n', text)
            title   = form.cleaned_data["title"]
            # save file
            util.save_entry(title, text)
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('entry', args=(title,)))
        else:
            print("FORM IS NOT VALID")
            print(request.POST['title'])
    # if a GET (or any other method) we'll create a blank form
    else:
        text = util.get_entry(name)
        pattern = r'\r\n'
        replacement = '\n'
        text = re.sub(pattern, replacement, text)
        form = entryForm({'title': name , 'text': text })
    return render(request, "encyclopedia/edit_entry.html", { 'form': form })


def randPage(request):
    tal = random.randint(0, len(util.list_entries())-1)
    name = util.list_entries()[tal]
    title = util.get_entry(name)
    return HttpResponseRedirect(reverse('entry', args=(name,)))
    