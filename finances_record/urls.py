from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from finances_record import views

urlpatterns = [
    path('expense-categories/', views.ExpenseCategoryList.as_view()),
    path('income-categories/', views.IncomeCategoryList.as_view()),
    path('cash-accounts/', views.CashAccountList.as_view()),
    path('expenses/', views.ExpenseEntryList.as_view()),
    path('incomes/', views.IncomeEntryList.as_view()),
    path('cash/', views.CashEntryList.as_view()),
    path('balance-summary/', views.BalanceSummaryList.as_view()),
    path('monthly-expense-summary/', views.MonthlyExpenseSummaryList.as_view()),
    path('monthly-income-summary/', views.MonthlyIncomeSummaryList.as_view()),
    path('payables/', views.PayableList.as_view()),
    path('receivables/', views.ReceivableList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)