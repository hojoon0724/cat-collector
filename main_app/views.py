from django.shortcuts import render, redirect
from .models import Cat, Toy
from django.views.generic import ListView, DetailView

# import the FeedingForm
from .forms import FeedingForm

# Add the following import
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def cat_index(request):
    cats = Cat.objects.order_by("id")
    return render(request, "cats/index.html", {"cats": cats})


def cats_detail(request, cat_id):
    # Get the individual cat
    cat = Cat.objects.get(id=cat_id)
    # instantiate the FeedingForm to be rendered in the template
    feeding_form = FeedingForm()
    # Render template, passing the cat data

    # Get the toys the cat doesn't have
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=cat.toys.all())

    return render(
        request,
        "cats/detail.html",
        {
            "cat": cat,
            "feeding_form": feeding_form,
            "toys": toys_cat_doesnt_have,
        },
    )


class CatCreate(CreateView):
    model = Cat
    # fields = "__all__"
    # or you can explicitly pick which fields
    fields = ["name", "breed", "description", "age"]
    success_url = "/cats/"


class CatUpdate(UpdateView):
    model = Cat
    # lets disallow renaming the cat
    fields = ["breed", "description", "age"]


class CatDelete(DeleteView):
    model = Cat
    success_url = "/cats/"


# FEEDINGS


def add_feeding(request, cat_id):
    # create the ModelForm using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
        # wait to save the cat in the db unit is has the cat_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()

    return redirect("detail", cat_id=cat_id)


class ToyList(ListView):
    model = Toy


class ToyDetail(DetailView):
    model = Toy


class ToyCreate(CreateView):
    model = Toy
    fields = "__all__"


class ToyUpdate(UpdateView):
    model = Toy
    fields = ["name", "color"]


class ToyDelete(DeleteView):
    model = Toy
    success_url = "/toys/"


def assoc_toy(request, cat_id, toy_id):
    # Note we can pass the toy's ID instead of the whole object
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect("detail", cat_id=cat_id)


def remove_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect("detail", cat_id=cat_id)
