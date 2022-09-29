from pyexpat import model
from django.db import models

# Create your models here.

class BalanceSummary(models.Model):
    payable_balance = models.IntegerField()
    receivable_balance = models.IntegerField()
    cash_balance = models.IntegerField()

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50)
    budget = models.IntegerField()

    def __str__(self):
        return self.name

class IncomeCategory(models.Model):
    name = models.CharField(max_length=50)
    target = models.IntegerField()

    def __str__(self):
        return self.name

class MonthlyExpenseSummary(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    expense_category = models.ForeignKey(ExpenseCategory, related_name='monthly_expense_summaries', on_delete=models.PROTECT)
    balance = models.IntegerField()

    def __str__(self):
        return str(self.year)+str(self.month)

class MonthlyIncomeSummary(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    income_category = models.ForeignKey(IncomeCategory, related_name='monthly_income_summaries', on_delete=models.PROTECT)
    balance = models.IntegerField()

    def __str__(self):
        return str(self.year)+str(self.month)

class CashAccount(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CashEntry(models.Model):
    cash_account = models.ForeignKey(CashAccount, related_name='cash_entries', on_delete=models.PROTECT)
    amount = models.IntegerField()
    description = models.CharField(max_length=100)
    date = models.DateField()


class ExpenseEntry(models.Model):
    expense_category = models.ForeignKey(ExpenseCategory, related_name='expense_entries', on_delete=models.PROTECT, )
    amount = models.IntegerField()
    description = models.CharField(max_length=100)
    date = models.DateField()
    monthly_summary = models.ForeignKey(MonthlyExpenseSummary, blank=True, null=True,  related_name='expense_entries', on_delete=models.PROTECT)
    cash_entry = models.ForeignKey(CashEntry, related_name='expense_entry', blank=True, null=True, on_delete=models.PROTECT)

class IncomeEntry(models.Model):
    income_category = models.ForeignKey(IncomeCategory, related_name='income_entries', on_delete=models.PROTECT)
    amount = models.IntegerField()
    description = models.CharField(max_length=100)
    date = models.DateField()
    monthly_summary = models.ForeignKey(MonthlyIncomeSummary, blank=True, null=True, related_name='income_entries', on_delete=models.PROTECT)
    cash_entry = models.ForeignKey(CashEntry, related_name='income_entry', blank=True, null=True, on_delete=models.PROTECT)


class Payable(models.Model):
    amount = models.IntegerField()
    paid = models.BooleanField(default=False)
    expense_entry = models.ForeignKey(ExpenseEntry, related_name='payables', on_delete=models.PROTECT)
    cash_entry = models.ForeignKey(CashEntry, related_name='payables', blank=True, null=True, on_delete=models.PROTECT)

class Receivable(models.Model):
    amount = models.IntegerField()
    paid = models.BooleanField(default=False)
    income_entry = models.ForeignKey(IncomeEntry, related_name='receivables', on_delete=models.PROTECT)
    cash_entry = models.ForeignKey(CashEntry, related_name='receivables', blank=True, null=True, on_delete=models.PROTECT)