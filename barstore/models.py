from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)

    cost_per_item = models.DecimalField(
        max_digits=19, decimal_places=2, null=False, blank=False)
    sales = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=False)
    quantity_damaged = models.IntegerField(default='0', blank=True, null=True)

    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)

    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)

    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.item_name


class StockHistory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)

    cost_per_item = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=False)
    sales = models.DecimalField(
        max_digits=19, decimal_places=2, null=True, blank=True)
    quantity_damaged = models.IntegerField(default='0', blank=True, null=True)

    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)

    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)

    last_updated = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True)
    timestamp = models.DateTimeField(
        auto_now_add=False, auto_now=False, null=True)
