from asyncore import write
from rest_framework import serializers
from finances_record.models import BalanceSummary, CashAccount, CashEntry, ExpenseCategory, ExpenseEntry, IncomeCategory, IncomeEntry, MonthlyExpenseSummary, MonthlyIncomeSummary, Payable, Receivable
from django.contrib.auth.models import User

class BalanceSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSummary
        fields = ['id', 'payable_balance', 'receivable_balance', 'cash_balance']

# class TransactionSerializer(serializers.ModelSerializer):
#     income_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=IncomeEntry.objects.all())
#     expense_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=ExpenseEntry.objects.all())
#     cash_entries = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

#     class Meta:
#         model = Transaction
#         fields = ['id', 'date', 'description', 'income_entries', 'expense_entries', 'cash_entries',]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']

class ExpenseCategorySerializer(serializers.ModelSerializer):
    monthly_expense_summaries = serializers.PrimaryKeyRelatedField(many=True, queryset=MonthlyExpenseSummary.objects.all())
    expense_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=ExpenseEntry.objects.all())

    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'budget', 'monthly_expense_summaries', 'expense_entries']
        # fields = ['id', 'name', 'budget', ]

class IncomeCategorySerializer(serializers.ModelSerializer):
    monthly_income_summaries = serializers.PrimaryKeyRelatedField(many=True, queryset=MonthlyIncomeSummary.objects.all())
    income_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=IncomeEntry.objects.all())

    class Meta:
        model = IncomeCategory
        fields = ['id', 'name', 'target', 'monthly_income_summaries', 'income_entries']

class MonthlyExpenseSummarySerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())
    category = ExpenseCategorySerializer(read_only=True)
    expense_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=ExpenseEntry.objects.all())

    class Meta:
        model = MonthlyExpenseSummary
        fields = ['id', 'month', 'year','category', 'balance', 'expense_entries']

class MonthlyIncomeSummarySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=IncomeCategory.objects.all())
    income_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=IncomeEntry.objects.all())

    class Meta:
        model = MonthlyIncomeSummary
        fields = ['id', 'month', 'year','category', 'balance', 'income_entries']

class CashAccountSerializer(serializers.ModelSerializer):
    cash_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=CashEntry.objects.all())

    class Meta:
        model = CashAccount
        fields = ['id', 'name', 'description', 'balance', 'cash_entries']

class ExpenseEntrySerializer(serializers.ModelSerializer):
    payables = serializers.PrimaryKeyRelatedField(many=True, queryset=Payable.objects.all())
    category = serializers.StringRelatedField()
    cash = serializers.BooleanField(write_only=True)
    cash_account = serializers.PrimaryKeyRelatedField(write_only=True ,queryset=CashAccount.objects.all())
    # transaction = serializers.PrimaryKeyRelatedField(queryset=Transaction.objects.all())
    # monthly_summary = serializers.PrimaryKeyRelatedField(queryset=MonthlyExpenseSummary.objects.all())

    class Meta:
        model = ExpenseEntry
        fields = ['id', 'category', 'date', 'description', 'amount',  'payables', 'cash', 'cash_account']


class IncomeEntrySerializer(serializers.ModelSerializer):
    receivables = serializers.PrimaryKeyRelatedField(many=True, queryset=Receivable.objects.all())
    category = serializers.StringRelatedField()
    cash = serializers.BooleanField(write_only=True)
    cash_account = serializers.PrimaryKeyRelatedField(write_only=True ,queryset=CashAccount.objects.all())
    # transaction = serializers.PrimaryKeyRelatedField(queryset=Transaction.objects.all())
    # monthly_summary = serializers.PrimaryKeyRelatedField(queryset=MonthlyIncomeSummary.objects.all())

    class Meta:
        model = IncomeEntry
        fields = ['id', 'category', 'date', 'description', 'amount', 'receivables', 'cash', 'cash_account']

class CashEntrySerializer(serializers.ModelSerializer):
    payables = serializers.PrimaryKeyRelatedField(many=True, queryset=Payable.objects.all())
    receivables = serializers.PrimaryKeyRelatedField(many=True, queryset=Receivable.objects.all())
    cash_account = serializers.PrimaryKeyRelatedField(queryset=CashAccount.objects.all())
    # transaction = serializers.PrimaryKeyRelatedField(queryset=Transaction.objects.all())

    class Meta:
        model = CashEntry
        fields = ['id', 'cash_account', 'date', 'description', 'amount', 'payables', 'receivables']

class PayableSerializer(serializers.ModelSerializer):
    entry = serializers.PrimaryKeyRelatedField(queryset=ExpenseEntry.objects.all())
    # cash_entry = serializers.PrimaryKeyRelatedField(queryset=CashEntry.objects.all(), required=False)
    cash_account = serializers.PrimaryKeyRelatedField(queryset=CashAccount.objects.all(), write_only=True)
    class Meta:
        model = Payable
        fields = ['id', 'description', 'amount', 'date', 'paid', 'payment_date', 'entry', 'cash_account']

class ReceivableSerializer(serializers.ModelSerializer):
    entry = serializers.PrimaryKeyRelatedField(queryset=IncomeEntry.objects.all())
    # cash_entry = serializers.PrimaryKeyRelatedField(queryset=CashEntry.objects.all(), required=False)
    cash_account = serializers.PrimaryKeyRelatedField(queryset=CashAccount.objects.all(), write_only=True)
    class Meta:
        model = Receivable
        fields = ['id', 'description', 'amount', 'date', 'paid', 'payment_date', 'entry', 'cash_account']