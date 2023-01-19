from django import forms
from barstore.models import Stock

# Create form to issue out sales


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_to']


# Create a form to record numbers of damaged products


class DamageForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['quantity_damaged']


# Create a form to receive new stocks
class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity']


# Create a form to set reorder level of product
class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']
