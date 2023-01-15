from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import csv
from django.contrib import messages
from .models import *
from .forms import *
# Display Landing Page.


@login_required
def home(request):
    title = 'Welcome: This is the Home Page'
    context = {
        "title": title,
    }
    return render(request, "home.html", context)


# List Out all the items from the database.
@login_required
def list_item(request):
    header = 'List of Items'

    # this for search functionality.
    form = StockSearchForm(request.POST or None)
    #
    """
    The reason i wrote the search logic inside the list item block:
        1. i want to search on the same page where my items are listed


    question for my future engineer:
        1. is this a good design.
        2. is this requied by the project manager/client.
        3. is there other ways to do it.
        4. will you do it again like this. ha!
    """

    queryset = Stock.objects.all()
    context = {
        "header":  header,
        "queryset": queryset,
        "form": form,
    }

    # create a condition for how the search wil work.
    if request.method == 'POST':
        queryset = Stock.objects.filter(  # category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value(
            )
        )
        # Make an if condition that will export data to CSV
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of Products.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                    [stock.category, stock.item_name, stock.quantity])
            return response
        context = {
            "form": form,
            "header": header,
            "queryset": queryset,
        }

    return render(request, "list_item.html", context)


# This code  adds items into the database.
@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Added')
        return redirect('../list_item')

    context = {
        "form": form,
        "header": "Add Item",
    }
    return render(request, "add_items.html", context)


# Create a Items Update view
@login_required
def update_items(request, pk):
    header = 'Update Item'
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully')
            return redirect('/barstore/list_item')

    context = {
        'form': form,
        'header':  header,
    }
    return render(request, 'add_items.html', context)


# Create a view to handle and process delete request.
@login_required
def delete_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        messages.success(request, 'Deleted Successfully')
        return redirect('/barstore/list_item')
    return render(request, 'delete_items.html')


# Create stock details view
@login_required
def stock_detail(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        "title": queryset.item_name,
        "queryset": queryset,
    }
    return render(request, "stock_detail.html", context)


# create
@login_required
def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity -= instance.issue_quantity
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) +
                         " " + str(instance.item_name) + "s now left in Store")
        instance.save()

        return redirect('/barstore/stock_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(queryset.item_name),
        "queryset": queryset,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)


#
@login_required
def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " +
                         str(instance.quantity) + " " + str(instance.item_name)+"s now in Store")

        return redirect('/barstore/stock_detail/'+str(instance.id))
        # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Reaceive ' + str(queryset.item_name),
        "instance": queryset,
        "form": form,
        "username": 'Receive By: ' + str(request.user),
    }
    return render(request, "add_items.html", context)


#
@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) +
                         " is updated to " + str(instance.reorder_level))

        return redirect('/barstore/list_item')
    context = {
        "instance": queryset,
        "form": form,
    }
    return render(request, "add_items.html", context)


#
@login_required
def list_history(request):
    header = 'LIST OF ITEMS'
    queryset = StockHistory.objects.all()
    context = {
        "header": header,
        "queryset": queryset,
    }
    return render(request, "list_history.html", context)
