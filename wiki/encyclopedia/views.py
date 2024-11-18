from django.shortcuts import render, redirect
from django.contrib import messages
from . import helpers
from . import util
from . import forms


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page(request, entry):
    return render(request, "encyclopedia/title.html", {
        "title": entry,
        "entry": util.get_entry(entry.upper())
    })


def searchresults(request):
    input = request.GET.get('q')
    if input.lower() in [title.lower() for title in util.list_entries()]:
        result = input.lower()
        return redirect(f"/wiki/{result}")
    # check if user input is a substring in saved entries
    result = helpers.search(input)
    # return all matches with the substr
    return render(request, "encyclopedia/index.html", {
        "entries": result
    })


def create_new_page(request):
    return render(request, "encyclopedia/createnewpage.html", {
        "NewArticle": forms.NewArticleForm()
    })


def edit_content(request, entry):
    if request.method == "POST":
        article = request.POST.get("article")
        util.save_entry(entry, article)
        return redirect(f"/wiki/{entry}")

    content = util.get_entry(entry.upper())
    return render(request, "encyclopedia/edit.html", {
        "title": entry,
        "EditArticle": forms.TitelDisabled({
            "title_disabled": entry,
            "article": content
            })
    })


def save_new_article(request):
    title = request.POST.get("title")
    article = request.POST.get("article")
    if title in util.list_entries():
        messages.error(request, f'Article with the title {title} already exists!')
        return render(request, "encyclopedia/createnewpage.html", {
            "NewArticle": forms.NewArticleForm({
                "title": title,
                "article": article
                }),
        })
    else:
        util.save_entry(title, article)
        return redirect(f"/wiki/{title}")


def random_page(request):
    random_article = helpers.random_article()
    return redirect(f"/wiki/{random_article}")
