from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import csv
from django.contrib import messages
from .models import *
from .forms import *
from sales.views import *


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
    header = 'List of Products'

    # this for search functionality.
    form = StockSearchForm(request.POST or None)
    #
    """
    The reason i wrote the search logic inside the list item block:
        1. we want to search on the same page where items are listed


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
        category = form['category'].value()
        queryset = Stock.objects.filter(  # category__icontains=form['category'].value(),
            item_name__icontains=form['item_name'].value(
            )
        )
        if (category != ''):
            queryset = queryset.filter(category_id=category)
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
        return redirect('list_item')

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
            return redirect('list_item')

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
        return redirect('list_item')
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


def add_category(request):
    form = CategoryCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully Created')
        return redirect('list_item')
    context = {
        "form": form,
        "title": "Add Category",
    }
    return render(request, "add_category.html", context)


'''CREATE TRIGGER after_barstore_stock_update AFTER UPDATE ON barstore_stock
BEGIN
		INSERT INTO barstore_stockhistory(
			id, 
			last_updated, 
			category_id, 
			item_name, 
			quantity, 
			receive_quantity, 
			receive_by) 
		VALUES(
			new.id, 
			new.last_updated, 
			new.category_id, 
			new.item_name, 
			new.quantity, 
			new.receive_quantity, 
			new.receive_by);


		INSERT INTO barstore_stockhistory(
			id, 
			last_updated, 
			category_id, 
			item_name, 
			issue_quantity, 
			issue_to, 
			issue_by, 
			quantity) 
		VALUES(
			new.id, 
			new.last_updated, 
			new.category_id, 
			new.item_name, 
			new.issue_quantity, 
			new.issue_to, 
			new.issue_by, 
			new.quantity);

END;'''


'''CREATE TRIGGER after_barstore_stock_update AFTER UPDATE ON barstore_stock
BEGIN
		INSERT INTO barstore_stockhistory(
			id, 
			last_updated, 
			category_id, 
			item_name, 
			quantity, 
            cost_per_item,
            sales ,
            quantity_damaged
			receive_quantity, 
			receive_by,
            issue_quantity, 
			issue_to, 
			issue_by, 
			quantity) 
		VALUES(
			new.id, 
			new.last_updated, 
			new.category_id, 
			new.item_name, 
			new.quantity, 
            new.cost_per_item,
            new.sales,
            new.quantity_damaged,
			new.receive_quantity, 
			new.receive_by,
            new.issue_quantity, 
			new.issue_to, 
			new.issue_by, 
			new.quantity);

END;'''
