from datetime import datetime
from django.shortcuts import render
from finances_record import serializers
from finances_record.models import BalanceSummary, CashEntry, ExpenseCategory, ExpenseEntry, IncomeEntry, MonthlyExpenseSummary, MonthlyIncomeSummary, Payable, Receivable, IncomeCategory, CashAccount
from finances_record.serializers import BalanceSummarySerializer, CashAccountSerializer, CashEntrySerializer, ExpenseCategorySerializer, ExpenseEntrySerializer, IncomeCategorySerializer, IncomeEntrySerializer, MonthlyExpenseSummarySerializer, MonthlyIncomeSummarySerializer, PayableSerializer, ReceivableSerializer
from rest_framework.response import Response
from rest_framework import status, generics

# from rest_framework import 

EXPENSE_ENTRY = 1
INCOME_ENTRY = 2
PAYABLE_ENTRY = 3
RECEIVABLE_ENTRY = 4

def _get_balance_summary(self):
    """
        Function to obtain balance summary item. If balance summary not yet created, it will create one.
        Always use this function to obtain balance summary.
    """
    try:
        return BalanceSummary.objects.get(pk=1)
    except BalanceSummary.DoesNotExist:
        return BalanceSummary.objects.create(payable_balance=0, receivable_balance=0, cash_balance=0)

def create_entry(self, serializer, summary, unpaid, entry_type):
        """
            Override perform_create to add monthly summary object into the expense and creating cash/payable entries.
            If no monthly summary, create new one.
            Add the expense amount into the summary balance.

            :param self: self object 
            :param serializer: serializer object
            :param summary: MonthlyExpenseSummary/MonthlyIncomeSummary class from models
            :param unpaid: Payable/Receivable class from models
            :param entry_type: constant to identify the user of this function
        """
        category = serializer.validated_data.get('category')
        date = serializer.validated_data.get('date')
        amount = serializer.validated_data.get('amount')
        description = serializer.validated_data.get('description')
        balance_summary = _get_balance_summary(self)

        try:
            item_summary =  summary.objects.get(year=date.year, month=date.month, category=category)
            item_summary.balance = item_summary.balance + amount
            item_summary.save()
        except summary.DoesNotExist:
            item_summary = summary.objects.create(year=date.year, month=date.month, category=category, balance=amount)
        
        cash_account = serializer.validated_data.pop('cash_account')
        if serializer.validated_data.pop('cash'):
            cash_amount = amount
            if entry_type == EXPENSE_ENTRY: cash_amount = -cash_amount
            cash_account.balance = cash_account.balance + cash_amount
            cash_account.save()
            balance_summary.cash_balance = balance_summary.cash_balance + cash_amount
            balance_summary.save()
            cash = CashEntry.objects.create(cash_account=cash_account, date=date, description=description, amount=cash_amount)
            serializer.save(monthly_summary = item_summary, cash_entry=cash)
        else:
            if entry_type == EXPENSE_ENTRY: balance_summary.payable_balance = balance_summary.payable_balance + amount
            if entry_type == INCOME_ENTRY: balance_summary.receivable_balance = balance_summary.receivable_balance + amount
            balance_summary.save()
            transaction = serializer.save(monthly_summary = item_summary)
            unpaid_item = unpaid.objects.create(amount=amount, date=date, description=description, paid=False, entry=transaction)
            unpaid_item.save()

def update_unpaid(self, serializer, entry_type):

    """
        Function to create payable/receivable payment or simply to update data.

        :param self: self object
        :param serializer: serializer object
        :param entry_type: constant to identify whether the function is called by payable/receivable
    """

    prev_instance = self.get_object()

    date = serializer.validated_data.get('payment_date')
    amount = serializer.validated_data.get('amount')
    description = serializer.validated_data.get('description')
    cash_account = serializer.validated_data.pop('cash_account')

    cash_amount = amount
    if entry_type == PAYABLE_ENTRY: cash_amount = -cash_amount

    # Check if previously not paid yet
    # If not paid, and the paid is True, then the update is to change the status from unpaid to paid
    if not prev_instance.paid and serializer.validated_data.get('paid'):
        print('-' * 10,'UPDATE TO CHANGE STATUS', '-' * 10)

        # Obtain cash account from validated data
        cash_account.balance = cash_account.balance + cash_amount
        cash_account.save() 

        cash = CashEntry.objects.create(date=date, amount=cash_amount, description=description, cash_account=cash_account)
        cash.save()

        # Obtain balance summary (Cash, Receivable, Payable) and update it
        balance_summary = _get_balance_summary(self)
        if entry_type == PAYABLE_ENTRY: balance_summary.payable_balance = balance_summary.payable_balance - amount
        if entry_type == RECEIVABLE_ENTRY: balance_summary.receivable_balance = balance_summary.receivable_balance - amount
        balance_summary.cash_balance = balance_summary.cash_balance + cash_amount
        balance_summary.save()

        serializer.save(cash_entry=cash)
    
    # Else, this will be a data update, but no change in payment status
    else:
        # If previous status was paid, update the balance
        if prev_instance.paid:
            # Obtain prev cash entry to update date & description
            cash = prev_instance.cash_entry
            cash.date = date
            cash.description = description

            # Update the balance if amount changed
            if prev_instance.amount != amount:
                # Calculate difference between new and previous amount
                delta = amount - prev_instance.amount
                delta_cash = cash_amount - cash.amount

                # Update cash entry amount
                cash.amount = cash.amount + delta_cash
                cash.save()

                # Obtain & update cash account balance
                cash_account = cash.cash_account
                cash_account.balance = cash_account.balance + delta_cash
                cash_account.save() 

                # Obtain & update balance summary
                balance_summary = _get_balance_summary(self)
                if entry_type == PAYABLE_ENTRY: balance_summary.payable_balance = balance_summary.payable_balance + delta
                if entry_type == RECEIVABLE_ENTRY: balance_summary.receivable_balance = balance_summary.receivable_balance + delta
                balance_summary.cash_balance = balance_summary.cash_balance + delta_cash
                balance_summary.save()
        
        serializer.save(cash_entry=cash)

# Create your views here.
class ExpenseCategoryList(generics.ListCreateAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

class ExpenseCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

class IncomeCategoryList(generics.ListCreateAPIView):
    queryset = IncomeCategory.objects.all()
    serializer_class = IncomeCategorySerializer

class IncomeCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IncomeCategory.objects.all()
    serializer_class = IncomeCategorySerializer

class CashAccountList(generics.ListCreateAPIView):
    queryset = CashAccount.objects.all()
    serializer_class = CashAccountSerializer

    def perform_create(self, serializer):
        amount = serializer.validated_data.get('balance')
        balance_summary = _get_balance_summary(self)
        balance_summary.cash_balance = balance_summary.cash_balance + amount
        balance_summary.save()

        serializer.save()

class ExpenseEntryList(generics.ListCreateAPIView):
    queryset = ExpenseEntry.objects.order_by('-date')
    serializer_class = ExpenseEntrySerializer

    def perform_create(self, serializer):
        create_entry(self, serializer, MonthlyExpenseSummary, Payable, EXPENSE_ENTRY)

class ExpenseEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExpenseEntry.objects.all()
    serializer_class = ExpenseEntrySerializer

class IncomeEntryList(generics.ListCreateAPIView):
    queryset = IncomeEntry.objects.order_by('-date')
    serializer_class = IncomeEntrySerializer
    
    def perform_create(self, serializer):
        create_entry(self, serializer, MonthlyIncomeSummary, Receivable, INCOME_ENTRY)

class IncomeEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = IncomeEntry.objects.all()
    serializer_class = IncomeEntrySerializer

class CashEntryList(generics.ListCreateAPIView):
    queryset = CashEntry.objects.all()
    serializer_class = CashEntrySerializer

class CashEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CashEntry.objects.order_by('-date')
    serializer_class = CashEntrySerializer

class BalanceSummaryList(generics.ListCreateAPIView):
    queryset = BalanceSummary.objects.all()
    serializer_class = BalanceSummarySerializer

class MonthlyExpenseSummaryList(generics.ListCreateAPIView):
    queryset = MonthlyExpenseSummary.objects.all()
    serializer_class = MonthlyExpenseSummarySerializer

    def get_queryset(self):
        year, month = self.kwargs.get('year'), self.kwargs.get('month')
        queryset = MonthlyExpenseSummary.objects.filter(year=year, month=month)
        
        return queryset

# class MonthlyExpenseSummaryList(generics.RetrieveUpdateDestroyAPIView):
#     queryset = MonthlyExpenseSummary.objects.all()
#     serializer_class = MonthlyExpenseSummarySerializer


class MonthlyIncomeSummaryList(generics.ListCreateAPIView):
    queryset = MonthlyIncomeSummary.objects.all()
    serializer_class = MonthlyIncomeSummarySerializer

    def get_queryset(self):
        year, month = self.kwargs.get('year'), self.kwargs.get('month')
        queryset = MonthlyIncomeSummary.objects.filter(year=year, month=month)
        
        return queryset

class PayableList(generics.ListCreateAPIView):
    queryset = Payable.objects.order_by('-date')
    serializer_class = PayableSerializer

    def get_queryset(self):
        queryset = Payable.objects.order_by('-date')
        unpaid = self.request.query_params.get('unpaid')
        if unpaid:
            queryset = Payable.objects.filter(paid=False).order_by('-date')
        return queryset

class PayableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payable.objects.all()
    serializer_class = PayableSerializer

    def perform_update(self, serializer):
        update_unpaid(self, serializer, PAYABLE_ENTRY)

class ReceivableList(generics.ListCreateAPIView):
    queryset = Receivable.objects.order_by('-date')
    serializer_class = ReceivableSerializer

class ReceivableDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receivable.objects.all()
    serializer_class = ReceivableSerializer
    
    def perform_update(self, serializer):
        update_unpaid(self, serializer, RECEIVABLE_ENTRY)
