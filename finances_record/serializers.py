from rest_framework import serializers
from finances_record.models import BalanceSummary, CashAccount, CashEntry, ExpenseCategory, ExpenseEntry, IncomeCategory, IncomeEntry, MonthlyExpenseSummary, MonthlyIncomeSummary, Payable, Receivable, Transaction
from django.contrib.auth.models import User

class BalanceSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSummary
        fields = ['id', 'payable_balance', 'receivable_balance', 'cash_balance']

class TransactionSerializer(serializers.ModelSerializer):
    income_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=IncomeEntry.objects.all())
    expense_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=ExpenseEntry.objects.all())
    cash_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=CashEntry.objects.all())

    class Meta:
        model = Transaction
        fields = ['id', 'date', 'description', 'income_entries', 'expense_entries', 'cash_entries',]

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
    expense_category = serializers.PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())
    expense_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=ExpenseEntry.objects.all())

    class Meta:
        model = MonthlyExpenseSummary
        fields = ['id', 'month', 'year','expense_category', 'balance', 'expense_entries']

class MonthlyIncomeSummarySerializer(serializers.ModelSerializer):
    income_category = serializers.PrimaryKeyRelatedField(queryset=IncomeCategory.objects.all())
    income_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=IncomeEntry.objects.all())

    class Meta:
        model = MonthlyIncomeSummary
        fields = ['id', 'month', 'year','income_category', 'balance', 'income_entries']

class CashAccountSerializer(serializers.ModelSerializer):
    cash_entries = serializers.PrimaryKeyRelatedField(many=True, queryset=CashEntry.objects.all())

    class Meta:
        model = CashAccount
        fields = ['id', 'name', 'cash_entries',]

class ExpenseEntrySerializer(serializers.ModelSerializer):
    payables = serializers.PrimaryKeyRelatedField(many=True, queryset=Payable.objects.all())
    expense_category = serializers.PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())
    transaction = serializers.PrimaryKeyRelatedField(queryset=Transaction.objects.all())
    monthly_summary = serializers.PrimaryKeyRelatedField(queryset=MonthlyExpenseSummary.objects.all())

    class Meta:
        model = ExpenseEntry
        fields = ['id', 'expense_category', 'amount','transaction', 'monthly_summary', 'payables']

class IncomeEntrySerializer(serializers.ModelSerializer):
    receivables = serializers.PrimaryKeyRelatedField(many=True, queryset=Receivable.objects.all())
    income_category = serializers.PrimaryKeyRelatedField(queryset=IncomeCategory.objects.all())
    transaction = serializers.PrimaryKeyRelatedField(queryset=Transaction.objects.all())
    monthly_summary = serializers.PrimaryKeyRelatedField(queryset=MonthlyIncomeSummary.objects.all())

    class Meta:
        model = IncomeEntry
        fields = ['id', 'income_category', 'amount','transaction', 'monthly_summary', 'receivables']

class CashEntrySerializer(serializers.ModelSerializer):
    payables = serializers.PrimaryKeyRelatedField(many=True, queryset=Payable.objects.all())
    receivables = serializers.PrimaryKeyRelatedField(many=True, queryset=Receivable.objects.all())
    cash_account = serializers.PrimaryKeyRelatedField(queryset=CashAccount.objects.all())
    transaction = serializers.PrimaryKeyRelatedField(queryset=Transaction.objects.all())

    class Meta:
        model = CashEntry
        fields = ['id', 'cash_account', 'amount','transaction', 'payables', 'receivables']

class PayableSerializer(serializers.ModelSerializer):
    expense_entry = serializers.PrimaryKeyRelatedField(queryset=ExpenseEntry.objects.all())
    cash_entry = serializers.PrimaryKeyRelatedField(queryset=CashEntry.objects.all())
    class Meta:
        model = Payable
        fields = ['id', 'amount', 'paid','expense_entry','cash_entry',]

class ReceivableSerializer(serializers.ModelSerializer):
    income_entry = serializers.PrimaryKeyRelatedField(queryset=IncomeEntry.objects.all())
    cash_entry = serializers.PrimaryKeyRelatedField(queryset=CashEntry.objects.all(), required=False)
    class Meta:
        model = Receivable
        fields = ['id', 'amount', 'paid','income_entry','cash_entry',]