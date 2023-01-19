from django import forms
from .models import *


# CUSTOMIZE THE ADMIN PORTAL FOR BETTER DATA VIEWING.
class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity', 'cost_per_item']

    # To prevent saving object with a blank category name.
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('This field is required')
        # Alerting and preventing the duplicate entry of category name.
        # for inventories in Stock.objects.all():
        #     if inventories.category == category:
        #         raise forms.ValidationError(
        #             str(category) + ' is already created')
        return category

    # To prevent saving object with a blank item name.
    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not item_name:
            raise forms.ValidationError('This field is required')
        return item_name


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# Create form for updating data


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity', 'cost_per_item']


class StockHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)

    class Meta:
        model = StockHistory
        fields = ['category', 'item_name', 'start_date', 'end_date']


# Create a form to search category and item names
class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)

    class Meta:
        model = Stock
        fields = ['category', 'item_name']
