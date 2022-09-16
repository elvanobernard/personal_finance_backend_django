from django.shortcuts import render
from finances_record.models import BalanceSummary, CashEntry, ExpenseCategory, ExpenseEntry, IncomeEntry, MonthlyExpenseSummary, MonthlyIncomeSummary, Payable, Receivable, Transaction, IncomeCategory, CashAccount
from finances_record.serializers import BalanceSummarySerializer, CashAccountSerializer, CashEntrySerializer, ExpenseCategorySerializer, ExpenseEntrySerializer, IncomeCategorySerializer, IncomeEntrySerializer, MonthlyExpenseSummarySerializer, MonthlyIncomeSummarySerializer, PayableSerializer, ReceivableSerializer, TransactionSerializer
from rest_framework import status, generics

# from rest_framework import 

# Create your views here.
class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class ExpenseCategoryList(generics.ListCreateAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

class IncomeCategoryList(generics.ListCreateAPIView):
    queryset = IncomeCategory.objects.all()
    serializer_class = IncomeCategorySerializer

class CashAccountList(generics.ListCreateAPIView):
    queryset = CashAccount.objects.all()
    serializer_class = CashAccountSerializer

class ExpenseEntryList(generics.ListCreateAPIView):
    queryset = ExpenseEntry.objects.all()
    serializer_class = ExpenseEntrySerializer

class IncomeEntryList(generics.ListCreateAPIView):
    queryset = IncomeEntry.objects.all()
    serializer_class = IncomeEntrySerializer

class CashEntryList(generics.ListCreateAPIView):
    queryset = CashEntry.objects.all()
    serializer_class = CashEntrySerializer

class BalanceSummaryList(generics.ListCreateAPIView):
    queryset = BalanceSummary.objects.all()
    serializer_class = BalanceSummarySerializer

class MonthlyExpenseSummaryList(generics.ListCreateAPIView):
    queryset = MonthlyExpenseSummary.objects.all()
    serializer_class = MonthlyExpenseSummarySerializer

class MonthlyIncomeSummaryList(generics.ListCreateAPIView):
    queryset = MonthlyIncomeSummary.objects.all()
    serializer_class = MonthlyIncomeSummarySerializer

class PayableList(generics.ListCreateAPIView):
    queryset = Payable.objects.all()
    serializer_class = PayableSerializer

class ReceivableList(generics.ListCreateAPIView):
    queryset = Receivable.objects.all()
    serializer_class = ReceivableSerializer

